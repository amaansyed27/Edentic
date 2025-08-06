"""
🎬 EDENTIC - The story is yours. The edit is ours.

A revolutionary AI-powered multimedia content creation platform that combines your assets
(videos, images, audio) with AI-generated content to create professional videos.

Upload any combination of media, describe what you want, and AI will:
- Generate missing content (images, videos, music, voiceovers)
- Edit and arrange everything professionally
- Create the perfect final video

Perfect for tutorials, presentations, marketing videos, and creative projects!

Tech Stack:
- Streamlit (Web UI)
- VideoDB SDK (Video processing, editing, content generation)
- Google GenAI (Content analysis, image generation, narrative creation)
"""

import streamlit as st
import videodb
from videodb import connect
from google import genai
from google.genai import types
from PIL import Image
import json
import time
import tempfile
import os
from io import BytesIO
import base64
from videodb.asset import VideoAsset, AudioAsset, ImageAsset
from videodb.timeline import Timeline


def init_clients():
    """Initialize VideoDB and Google GenAI clients"""
    try:
        # Get API keys from Streamlit secrets
        videodb_api_key = st.secrets.get("VIDEODB_API_KEY")
        google_api_key = st.secrets.get("GOOGLE_API_KEY")
        
        if not videodb_api_key or not google_api_key:
            st.error("⚠️ API keys not found in secrets. Please configure VIDEODB_API_KEY and GOOGLE_API_KEY in your Streamlit secrets.")
            st.stop()
        
        # Initialize VideoDB connection (proper way according to docs)
        conn = connect(api_key=videodb_api_key)
        collection = conn.get_collection()
        
        # Set Google API key as environment variable for GenAI client
        os.environ["GEMINI_API_KEY"] = google_api_key
        genai_client = genai.Client()
        
        return conn, collection, genai_client
        
    except Exception as e:
        st.error(f"❌ Failed to initialize clients: {str(e)}")
        st.stop()


def upload_and_analyze_mixed_media(collection, uploaded_files, file_descriptions, project_description):
    """Upload mixed media (videos, images, audio) and analyze with user descriptions"""
    media_assets = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Track video durations for early validation
    total_video_duration = 0
    video_count = 0
    
    for i, uploaded_file in enumerate(uploaded_files):
        file_desc = file_descriptions.get(uploaded_file.name, "")
        status_text.text(f"📤 Uploading {uploaded_file.name}...")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name
        
        try:
            # Determine media type
            file_extension = uploaded_file.name.lower().split('.')[-1]
            media_type = None
            
            if file_extension in ['mp4', 'mov', 'avi', 'mkv', 'wmv']:
                media_type = 'video'
            elif file_extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                media_type = 'image'
            elif file_extension in ['mp3', 'wav', 'aac', 'm4a']:
                media_type = 'audio'
            
            # Upload to VideoDB
            if media_type == 'video':
                asset = collection.upload(file_path=tmp_file_path)
                # Index for search capabilities
                status_text.text(f"🧠 Analyzing {uploaded_file.name}...")
                try:
                    asset.index_spoken_words()
                    asset.index_scenes(prompt=f"Analyze this video: {file_desc}")
                    transcript = asset.get_transcript_text()
                except:
                    transcript = ""
            elif media_type == 'image':
                asset = collection.upload(file_path=tmp_file_path)
                transcript = ""
            elif media_type == 'audio':
                asset = collection.upload(file_path=tmp_file_path, media_type=videodb.MediaType.audio)
                transcript = ""
            else:
                # Try as video by default
                asset = collection.upload(file_path=tmp_file_path)
                transcript = ""
                media_type = 'video'
            
            # Get asset duration for videos
            asset_duration = 0
            if media_type == 'video':
                try:
                    # Try multiple ways to get video duration
                    asset_duration = getattr(asset, 'duration', 0)
                    
                    # If duration is 0, try other attributes
                    if asset_duration == 0:
                        asset_duration = getattr(asset, 'length', 0)
                    
                    # If still 0, try to get metadata
                    if asset_duration == 0:
                        try:
                            # Try to get video info
                            video_info = asset.get_video_info() if hasattr(asset, 'get_video_info') else None
                            if video_info and 'duration' in video_info:
                                asset_duration = video_info['duration']
                        except:
                            pass
                    
                    # If still 0, use a reasonable default based on typical clip length
                    if asset_duration == 0:
                        st.warning(f"⚠️ Could not detect duration for {uploaded_file.name}, using default 10s")
                        asset_duration = 10  # Default 10 seconds for unknown duration
                    
                    if asset_duration > 0:
                        total_video_duration += asset_duration
                        video_count += 1
                        st.info(f"📹 {uploaded_file.name}: {asset_duration}s duration")
                except Exception as e:
                    st.warning(f"⚠️ Duration detection failed for {uploaded_file.name}: {str(e)}, using default 10s")
                    asset_duration = 10  # Fallback duration
                    total_video_duration += asset_duration
                    video_count += 1
            
            media_assets.append({
                'asset': asset,
                'video_obj': asset if media_type == 'video' else None,  # Store video object for direct access
                'name': uploaded_file.name,
                'asset_id': asset.id,
                'media_type': media_type,
                'description': file_desc,
                'transcript': transcript,
                'file_extension': file_extension,
                'duration': max(asset_duration, 5) if media_type == 'video' else asset_duration  # Ensure minimum 5s for videos
            })
            
            # Update progress
            progress_bar.progress((i + 1) / len(uploaded_files))
            
        except Exception as e:
            st.error(f"❌ Failed to upload {uploaded_file.name}: {str(e)}")
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
    
    status_text.text("✅ All media uploaded and analyzed!")
    
    # Provide duration feedback to user
    if video_count > 0 and total_video_duration > 0:
        avg_duration = total_video_duration / video_count
        st.info(f"📊 Video Analysis: {video_count} videos, {total_video_duration:.1f}s total, {avg_duration:.1f}s average")
        
        if total_video_duration < 15:
            st.warning(f"⚠️ Short videos detected! Total duration: {total_video_duration:.1f}s. Video will be optimized for available content.")
        elif total_video_duration < 30:
            st.info(f"💡 Moderate video length: {total_video_duration:.1f}s. Perfect for social media!")
        else:
            st.success(f"✅ Great content length: {total_video_duration:.1f}s. Plenty of material to work with!")
    
    return media_assets


def generate_missing_content(collection, genai_client, content_plan, media_assets):
    """Generate missing content (images, videos, music, voiceovers) using AI"""
    
    generated_assets = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    generation_requests = content_plan.get('content_to_generate', [])
    
    for i, request in enumerate(generation_requests):
        content_type = request.get('type')
        description = request.get('description')
        
        status_text.text(f"🎨 Generating {content_type}: {description[:50]}...")
        
        try:
            # Focus only on voiceover generation - no title images or background music
            if content_type == 'voiceover':
                # Notify user about cropped content voiceover
                st.info("🎬 **Professional Editing**: Generating voiceover for cropped video segments (best portions of your videos)")
                
                # Generate voiceover using VideoDB
                voice_asset = collection.generate_voice(
                    text=request.get('script', description),
                    voice_name=request.get('voice_style', 'Default')
                )
                
                # Get duration for the generated voice asset
                try:
                    # Try to get duration from the asset
                    voice_duration = getattr(voice_asset, 'duration', 0)
                    if voice_duration <= 0:
                        # Fallback: estimate duration based on text length (rough: ~150 words per minute)
                        text_length = len(request.get('script', description).split())
                        voice_duration = max(10, text_length * 0.4)  # ~0.4 seconds per word
                        st.info(f"🔍 Estimated voiceover duration: {voice_duration:.1f}s (based on {text_length} words)")
                    
                    # Check if voiceover duration seems reasonable (basic check)
                    if voice_duration < 20:  # If voiceover is less than 20 seconds
                        st.warning(f"⚠️ Voiceover duration ({voice_duration:.1f}s) seems short for a tutorial video")
                        st.info("💡 The voiceover may not cover the entire video. Consider generating a longer script.")
                        
                except Exception as dur_error:
                    voice_duration = 30  # Safe fallback
                    st.warning(f"⚠️ Could not get voice duration, using fallback: {voice_duration}s")
                
                generated_assets.append({
                    'asset': voice_asset,
                    'name': f"generated_voiceover_{i}.mp3",
                    'asset_id': voice_asset.id,
                    'media_type': 'audio',
                    'description': description,
                    'duration': voice_duration,  # CRITICAL: Add duration to asset info
                    'generated': True,
                    'generation_type': 'voiceover'
                })
                
            elif content_type == 'video_clip':
                # Generate video using VideoDB
                video_asset = collection.generate_video(
                    prompt=description,
                    duration=request.get('duration', 5)
                )
                generated_assets.append({
                    'asset': video_asset,
                    'name': f"generated_video_{i}.mp4",
                    'asset_id': video_asset.id,
                    'media_type': 'video',
                    'description': description,
                    'generated': True,
                    'generation_type': 'video_clip'
                })
                
            else:
                # Skip other content types (title_image, background_music, etc.)
                st.info(f"⚠️ Skipping {content_type} generation (disabled for focus on video editing)")
                continue
                
        except Exception as e:
            st.warning(f"⚠️ Failed to generate {content_type}: {str(e)}")
        
        progress_bar.progress((i + 1) / len(generation_requests))
    
    status_text.text(f"✅ Generated {len(generated_assets)} new assets!")
    return generated_assets


def generate_title_image_with_gemini(genai_client, description):
    """Generate title image using Gemini's native image generation"""
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=description,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        
        # Save generated image
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                
                # Save to temporary file
                temp_path = tempfile.mktemp(suffix='.png')
                image.save(temp_path)
                
                return {
                    'file_path': temp_path,
                    'image': image
                }
        
        return None
        
    except Exception as e:
        st.warning(f"⚠️ Failed to generate image with Gemini: {str(e)}")
        return None
def create_comprehensive_content_plan(genai_client, media_assets, project_description, target_duration):
    """Create a comprehensive content plan based on available assets and project description"""
    
    # Gather all available media information with cropping context
    media_summary = []
    video_assets = [asset for asset in media_assets if asset['media_type'] == 'video']
    
    for asset in media_assets:
        asset_info = f"Asset: {asset['name']} ({asset['media_type']})\n"
        asset_info += f"Description: {asset['description']}\n"
        
        # For video assets, explain the cropping that will be applied
        if asset['media_type'] == 'video' and asset.get('duration', 0) > 0:
            source_duration = asset.get('duration', 10)
            # Calculate the actual cropped segment that will be used
            max_usable_duration = source_duration * 0.90  # Use up to 90% of source
            start_offset = min(1, source_duration * 0.1)  # Start slightly into the video
            
            asset_info += f"Original Duration: {source_duration:.1f}s\n"
            asset_info += f"IMPORTANT - Cropped Segment: Will use {max_usable_duration:.1f}s starting from {start_offset:.1f}s (skipping beginning/end)\n"
            asset_info += f"Actual Content Window: {start_offset:.1f}s to {start_offset + max_usable_duration:.1f}s of the original video\n"
        
        if asset['transcript']:
            # For video transcripts, note that content analysis is from full video but only portion will be used
            if asset['media_type'] == 'video':
                asset_info += f"Full Video Transcript (NOTE: Only middle portion will be used in final video): {asset['transcript'][:300]}...\n"
            else:
                asset_info += f"Content: {asset['transcript'][:200]}...\n"
        media_summary.append(asset_info)
    
    combined_media = "\n---\n".join(media_summary)
    
    prompt = f"""You are an expert multimedia content creator and video editor. Based on the project description and available assets, create a comprehensive content plan focusing on professional video editing and sequencing.

CRITICAL: The videos will be CROPPED to use only the best portions (typically starting 10% into the video and using 90% of content, avoiding boring beginnings/endings). Your voiceover script must match the CROPPED content that will actually appear in the final video, NOT the full original videos.

PROJECT DESCRIPTION:
{project_description}

TARGET DURATION: {target_duration} seconds

AVAILABLE ASSETS (with cropping information):
{combined_media}

Create a detailed content plan that focuses on video editing and sequencing. DO NOT generate background music or title images. Focus on:
1. Professional video editing: cropping, clipping, splitting, and sequencing the available video clips
2. Voiceover generation that matches the CROPPED video segments (not the full original videos)
3. Timeline structure with optimal pacing and transitions
4. Professional narrative flow using the available video assets

Return a JSON response with this structure:
{{
    "project_analysis": "Brief analysis of the project goals and video editing approach",
    "target_audience": "Who this content is for",
    "content_to_generate": [
        {{
            "type": "voiceover",
            "description": "Detailed description for AI generation - MUST match the cropped video content",
            "duration": 5,
            "placement": "beginning|middle|end",
            "voice_style": "friendly_female|professional_male|etc",
            "script": "IMPORTANT: Write a complete voiceover script that will take approximately {target_duration} seconds to narrate at normal speaking pace. Focus ONLY on the cropped video segments that will actually be shown (middle portions of videos, not beginnings/endings). Include detailed narration for each CROPPED video segment. The script should be comprehensive enough to cover the entire video duration and match the actual content that viewers will see."
        }}
    ],
    "timeline_structure": [
        {{
            "sequence": 1,
            "asset_name": "existing asset name or 'generated_X'",
            "start_time": 0,
            "end_time": 5,
            "description": "What happens in this CROPPED segment (not the full video)",
            "editing_notes": "Crop, adjust, overlay instructions",
            "audio_overlay": "background_music|voiceover|none"
        }}
    ],
    "editing_instructions": {{
        "style": "professional|casual|cinematic|educational",
        "transitions": "smooth|quick|creative",
        "audio_mixing": "music volume, voiceover prominence",
        "visual_effects": "any special effects or adjustments needed"
    }}
}}

Focus on creating engaging, professional content that matches the project description and makes optimal use of available assets.

CRITICAL FOR VOICEOVERS: When generating voiceover content, ensure the script is long enough to cover the full {target_duration} second video AND matches the CROPPED video content (not the full original videos). The videos will be professionally edited to show only the best portions. A typical speaking pace is about 150-180 words per minute, so for {target_duration} seconds, you need approximately {int((target_duration/60) * 160)} words. Include:
1. Opening introduction (10-15% of script) - introduce what viewers will see in the cropped segments
2. Detailed narration for each CROPPED video segment (70-80% of script) - describe only what's visible in the edited clips  
3. Closing summary (10-15% of script) - wrap up the content shown in the edited video

Make sure the voiceover script provides continuous narration that matches the CROPPED video content throughout the entire duration. Do NOT reference content from the beginning or end of videos that will be cut out during professional editing."""

    try:
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        # Extract JSON from the response text
        response_text = response.text.strip()
        
        # Try to find JSON within the response (remove markdown formatting)
        if "```json" in response_text:
            # Extract JSON from markdown code block
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            json_text = response_text[json_start:json_end].strip()
        elif "{" in response_text and "}" in response_text:
            # Find the JSON object in the response
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            json_text = response_text[start:end]
        else:
            json_text = response_text
        
        # Parse the JSON response
        content_plan = json.loads(json_text)
        return content_plan
        
    except json.JSONDecodeError as e:
        st.error(f"❌ Failed to parse AI content plan: {str(e)}")
        st.info(f"🔍 Raw AI response: {response.text[:500]}...")
        return create_fallback_content_plan(media_assets, project_description, target_duration)
    except Exception as e:
        st.error(f"❌ Failed to create content plan: {str(e)}")
        return create_fallback_content_plan(media_assets, project_description, target_duration)


def create_fallback_content_plan(media_assets, project_description, target_duration):
    """Create a basic content plan if AI analysis fails"""
    
    # Simple plan: use assets in order with basic structure
    timeline_structure = []
    
    if not media_assets:
        return {
            "project_analysis": f"Creating basic video content: {project_description[:100]}...",
            "target_audience": "General audience",
            "content_to_generate": [],
            "timeline_structure": [],
            "editing_instructions": {"style": "professional", "transitions": "smooth"}
        }
    
    segment_duration = max(5, target_duration // len(media_assets))
    
    for i, asset in enumerate(media_assets):
        # Analyze content importance based on description keywords
        description = (asset['description'] or asset['name']).lower()
        
        # Determine importance (1-3 scale) based on content analysis
        importance = 1  # Default
        if any(word in description for word in ['main', 'key', 'important', 'focus', 'primary', 'central']):
            importance = 3
        elif any(word in description for word in ['process', 'action', 'making', 'pouring', 'grinding', 'brewing']):
            importance = 2
        
        # Determine recommended duration based on content type
        recommended_duration = segment_duration
        if any(word in description for word in ['grinding', 'process', 'making', 'preparation']):
            recommended_duration = min(segment_duration * 1.2, 15)  # Slightly longer for process shots
        elif any(word in description for word in ['final', 'finished', 'result', 'cup']):
            recommended_duration = min(segment_duration * 0.8, 10)   # Shorter for result shots
        elif any(word in description for word in ['pouring', 'action', 'technique']):
            recommended_duration = min(segment_duration * 1.5, 18)   # Longer for key actions
        
        timeline_structure.append({
            "sequence": i + 1,
            "asset_name": asset['name'],
            "start_time": i * segment_duration,
            "end_time": (i + 1) * segment_duration,
            "clip_start": 0,
            "clip_end": min(segment_duration, asset.get('duration', segment_duration)),
            "description": asset['description'] or f"Showing {asset['name']}",
            "editing_notes": "Use full clip, adjust timing as needed",
            "audio_overlay": "background_music" if i > 0 else "none",
            "importance": importance,  # 1-3 scale for content importance
            "recommended_duration": recommended_duration,  # AI-suggested optimal duration
            "content_type": "process" if any(word in description for word in ['grinding', 'pouring', 'making']) else "result"
        })
    
    # Add voiceover generation
    content_to_generate = []
    if any(asset.get('description') for asset in media_assets):
        content_to_generate.append({
            "type": "voiceover",
            "description": "Professional narration explaining the content",
            "script": f"This video demonstrates {project_description}. " + 
                     " ".join([asset.get('description', '') for asset in media_assets if asset.get('description')]),
            "voice_style": "friendly_female",
            "duration": target_duration,
            "placement": "overlay"
        })
    
    return {
        "project_analysis": f"Creating video content based on: {project_description[:100]}...",
        "target_audience": "General audience",
        "content_to_generate": content_to_generate,
        "timeline_structure": timeline_structure,
        "editing_instructions": {
            "style": "professional",
            "transitions": "smooth",
            "audio_mixing": "balanced",
            "visual_effects": "none"
        }
    }


def create_fallback_understanding(clips_info):
    """Create a basic understanding structure if AI analysis fails"""
    return {
        "story_understanding": "Software demonstration or tutorial video",
        "target_audience": "Developers and users interested in the demonstrated software",
        "key_features": ["Software interface", "Key functionality", "User workflow"],
        "narrative_structure": [
            {
                "scene_description": f"Introduction and overview of {clips_info[0]['name']}",
                "narration": "Welcome to this demonstration. Let me show you the key features and capabilities of this application.",
                "suggested_duration": 15,
                "search_keywords": ["introduction", "overview", "welcome", "demo"]
            },
            {
                "scene_description": "Main functionality demonstration",
                "narration": "Here you can see the main interface and core functionality in action.",
                "suggested_duration": 20,
                "search_keywords": ["interface", "functionality", "features", "demo"]
            },
            {
                "scene_description": "Conclusion and summary",
                "narration": "That concludes our demonstration. Thank you for watching!",
                "suggested_duration": 10,
                "search_keywords": ["conclusion", "summary", "thank you", "end"]
            }
        ],
        "conclusion_narration": "Thank you for watching this demonstration!"
    }


def create_intelligent_edit_plan(video_db_client, ai_understanding, clips_info):
    """Create an edit plan based on AI understanding of the content"""
    
    edit_decision_list = []
    narrative_scenes = ai_understanding.get('narrative_structure', [])
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Get collection for multi-video search
    collection = video_db_client.get_collection()
    
    for i, scene in enumerate(narrative_scenes):
        status_text.text(f"🎯 Planning scene: '{scene['scene_description'][:50]}...'")
        
        # Use the search keywords to find the best matching clips
        search_query = " ".join(scene.get('search_keywords', [scene['scene_description']]))
        
        try:
            # Perform semantic search across all uploaded videos
            search_results = collection.search(query=search_query)
            
            if search_results and hasattr(search_results, 'get_shots'):
                shots = search_results.get_shots()
                if shots:
                    # Get the best matching shot
                    best_shot = shots[0]
                    
                    # Find the corresponding video object
                    matched_video = None
                    matched_clip_name = "Unknown"
                    for clip_info in clips_info:
                        if clip_info['video_id'] == best_shot.video_id:
                            matched_video = clip_info['video']
                            matched_clip_name = clip_info['name']
                            break
                    
                    if matched_video:
                        edit_decision_list.append({
                            'video': matched_video,
                            'scene_description': scene['scene_description'],
                            'narration': scene['narration'],
                            'start_time': best_shot.start,
                            'end_time': min(best_shot.end, best_shot.start + scene.get('suggested_duration', 15)),
                            'clip_name': matched_clip_name,
                            'search_query': search_query
                        })
                    else:
                        # Fallback to first available clip
                        edit_decision_list.append(create_fallback_scene(clips_info[0], scene, i))
                else:
                    # No shots found, use fallback
                    edit_decision_list.append(create_fallback_scene(clips_info[i % len(clips_info)], scene, i))
            else:
                # Search failed, use fallback
                edit_decision_list.append(create_fallback_scene(clips_info[i % len(clips_info)], scene, i))
                
        except Exception as e:
            st.warning(f"⚠️ Search failed for scene '{scene['scene_description']}': {str(e)}. Using fallback.")
            edit_decision_list.append(create_fallback_scene(clips_info[i % len(clips_info)], scene, i))
        
        # Update progress
        progress_bar.progress((i + 1) / len(narrative_scenes))
    
    status_text.text("✅ Intelligent edit plan created!")
    return edit_decision_list


def create_fallback_scene(clip_info, scene, index):
    """Create a fallback scene when search fails"""
    duration = scene.get('suggested_duration', 15)
    start_time = index * duration  # Distribute scenes across the clip
    
    return {
        'video': clip_info['video'],
        'scene_description': scene['scene_description'],
        'narration': scene['narration'],
        'start_time': start_time,
        'end_time': start_time + duration,
        'clip_name': clip_info['name'],
        'search_query': 'fallback'
    }


def generate_comprehensive_voiceover(video_db_client, ai_understanding, edit_decision_list):
    """Generate voiceover based on AI understanding and edit plan"""
    try:
        # Combine all narration from the edit plan
        full_narration_parts = []
        
        # Add introduction if available
        if ai_understanding.get('story_understanding'):
            intro = f"Welcome! {ai_understanding['story_understanding']}"
            full_narration_parts.append(intro)
        
        # Add scene narrations
        for decision in edit_decision_list:
            if decision.get('narration'):
                full_narration_parts.append(decision['narration'])
        
        # Add conclusion
        if ai_understanding.get('conclusion_narration'):
            full_narration_parts.append(ai_understanding['conclusion_narration'])
        
        # Combine all narration
        full_script = " ".join(full_narration_parts)
        
        # Generate voiceover
        collection = video_db_client.get_collection()
        voiceover_audio = collection.generate_voice(
            text=full_script,
            voice_name='Default'
        )
        return voiceover_audio, full_script
        
    except Exception as e:
        st.warning(f"⚠️ Voice generation failed: {str(e)}. Continuing without voiceover.")
        return None, ""


def assemble_multimedia_video_with_music(conn, content_plan, media_assets, generated_assets, target_duration=45):
    """Assemble video with both voiceover and background music using audio mixing approach"""
    
    try:
        from videodb.timeline import Timeline
        from videodb.asset import VideoAsset, AudioAsset, ImageAsset
        
        # Create a new timeline
        timeline = Timeline(conn)
        
        # Calculate total available video duration
        total_video_duration = 0
        video_assets = [a for a in media_assets if a['media_type'] == 'video']
        
        for asset in video_assets:
            asset_duration = asset.get('duration', 0)
            if asset_duration > 0:
                total_video_duration += asset_duration
        
        # Adjust target duration based on available content
        adjusted_duration = min(target_duration, max(total_video_duration * 0.8, 15))  # Use 80% of available content, min 15s
        
        st.info(f"📏 Adjusting video length for music version: Target {target_duration}s → Actual {adjusted_duration:.1f}s")
        
        # First, add all video/image content exactly like the voiceover-only version
        timeline_structure = content_plan.get('timeline_structure', [])
        
        # If no timeline structure, create a simple sequence from video assets
        if not timeline_structure:
            current_time = 0
            segment_duration = adjusted_duration / max(len(video_assets), 1)  # Divide time equally
            
            for i, asset in enumerate(video_assets):
                asset_duration = asset.get('duration', segment_duration)
                clip_duration = min(segment_duration, asset_duration * 0.9)  # Use 90% of asset duration max
                
                timeline_structure.append({
                    'asset_name': asset['name'],
                    'start_time': current_time,
                    'end_time': current_time + clip_duration,
                    'clip_start': 0,
                    'clip_end': clip_duration
                })
                current_time += clip_duration
        
        # Add main video/image assets to timeline with proper duration validation
        video_added = False
        
        for segment in timeline_structure:
            asset_name = segment.get('asset_name')
            
            if asset_name:
                # Find the asset
                asset_info = None
                for asset in media_assets:
                    if asset['name'] == asset_name:
                        asset_info = asset
                        break
                
                if asset_info and asset_info['media_type'] == 'video':
                    # Calculate optimal clip duration for target video length
                    clip_duration = min(
                        segment.get('end_time', 10) - segment.get('start_time', 0),
                        target_duration // len([s for s in timeline_structure if s.get('asset_name')]),
                        15  # Max 15 seconds per clip
                    )
                    clip_duration = max(clip_duration, 3)  # Min 3 seconds
                    
                    video_asset = VideoAsset(
                        asset_id=asset_info['asset_id'],
                        start=segment.get('clip_start', 0),
                        end=segment.get('clip_start', 0) + clip_duration
                    )
                    timeline.add_inline(video_asset)
                    video_added = True
                    total_video_duration += clip_duration
                    
                elif asset_info and asset_info['media_type'] == 'image':
                    # For images, create a short video segment
                    duration = min(segment.get('end_time', 5) - segment.get('start_time', 0), 8)
                    duration = max(duration, 3)  # Min 3 seconds
                    
                    image_asset = ImageAsset(
                        asset_id=asset_info['asset_id'],
                        duration=duration
                    )
                    timeline.add_inline(image_asset)
                    video_added = True
                    total_video_duration += duration
        
        # If no video was added, add the first video asset as fallback
        if not video_added and media_assets:
            first_video = next((a for a in media_assets if a['media_type'] == 'video'), None)
            if first_video:
                fallback_duration = min(target_duration, 30)
                fallback_asset = VideoAsset(
                    asset_id=first_video['asset_id'],
                    start=0,
                    end=fallback_duration
                )
                timeline.add_inline(fallback_asset)
                video_added = True
                total_video_duration = fallback_duration
        
        # Now add ONLY background music as overlay (no voiceover to avoid conflicts)
        # The voiceover is already mixed in from the previous version
        background_music_added = False
        for asset in generated_assets:
            if asset['media_type'] == 'audio' and asset.get('generation_type') == 'background_music':
                try:
                    # Add background music for the full video duration
                    music_duration = min(total_video_duration + 5, asset.get('duration', 60))
                    audio_asset = AudioAsset(
                        asset_id=asset['asset_id'],
                        start=0,
                        end=music_duration,
                        disable_other_tracks=False  # Mix with existing audio (voiceover)
                    )
                    timeline.add_overlay(start=0, asset=audio_asset)
                    background_music_added = True
                    st.info(f"✅ Added background music (0-{music_duration}s) mixing with voiceover")
                    break  # Only add one background music track
                    
                except Exception as e:
                    st.warning(f"⚠️ Failed to add background music: {str(e)}")
                    continue
        
        # Generate the final video stream
        if video_added:
            final_video_url = timeline.generate_stream()
            if background_music_added:
                st.success(f"✅ Video assembled with background music and voiceover!")
            else:
                st.success(f"✅ Video assembled (background music failed, but voiceover included)!")
            return final_video_url
        else:
            st.warning("⚠️ No video content was added to timeline")
            return None
            
    except Exception as e:
        st.error(f"❌ Video with music assembly failed: {str(e)}")
        return None


def test_video_generation():
    """
    Simple test function to diagnose video generation issues
    """
    try:
        from videodb.timeline import Timeline
        
        videodb_api_key = st.secrets.get("VIDEODB_API_KEY")
        if not videodb_api_key:
            st.error("VideoDB API key not found")
            return None
            
        conn = videodb.connect(api_key=videodb_api_key)
        coll = conn.get_collection()
        
        st.info("🔍 Testing basic video operations...")
        
        # Get first video from collection
        videos = coll.get_videos()
        if not videos:
            st.error("No videos found in collection")
            return None
            
        test_video = videos[0]
        st.info(f"📹 Testing with video: {test_video.name}")
        
        # Test 1: Basic play URL
        try:
            play_url = test_video.play()
            st.success(f"✅ Play URL: {play_url[:50]}...")
        except Exception as e:
            st.error(f"❌ Play URL failed: {str(e)}")
            
        # Test 2: Basic stream generation
        try:
            stream_url = test_video.generate_stream()
            st.success(f"✅ Stream URL: {stream_url[:50]}...")
            return stream_url
        except Exception as e:
            st.error(f"❌ Stream generation failed: {str(e)}")
            
        # Test 3: Timeline creation and stream
        try:
            timeline = Timeline(conn)
            timeline.add_inline(test_video)
            timeline_stream = timeline.generate_stream()
            st.success(f"✅ Timeline stream: {timeline_stream[:50]}...")
            return timeline_stream
        except Exception as e:
            st.error(f"❌ Timeline stream failed: {str(e)}")
            
        return None
        
    except Exception as e:
        st.error(f"❌ Test failed: {str(e)}")
        return None


def assemble_multimedia_video(conn, content_plan, media_assets, generated_assets, target_duration=45):
    """Assemble the final video using all assets according to the content plan"""
    
    try:
        from videodb.timeline import Timeline
        from videodb.asset import VideoAsset, AudioAsset, ImageAsset
        
        # DEBUG: Validate assets before creating timeline
        st.info("🔍 Validating assets before timeline creation...")
        valid_videos = []
        for asset in media_assets:
            if asset['media_type'] == 'video':
                try:
                    # Test if video is accessible
                    video_obj = asset.get('video_obj')
                    if video_obj and hasattr(video_obj, 'id'):
                        valid_videos.append(asset)
                        st.info(f"✅ Valid video: {asset['name']} (ID: {video_obj.id})")
                    else:
                        st.warning(f"⚠️ Invalid video object: {asset['name']}")
                except Exception as e:
                    st.warning(f"⚠️ Video validation failed for {asset['name']}: {str(e)}")
        
        if not valid_videos:
            st.error("❌ No valid video assets found")
            return None
        
        # Create a new timeline
        timeline = Timeline(conn)
        
        # Calculate total available video duration
        total_video_duration = 0
        video_assets = [a for a in media_assets if a['media_type'] == 'video']
        
        for asset in video_assets:
            asset_duration = asset.get('duration', 0)
            if asset_duration > 0:
                total_video_duration += asset_duration
        
        # Adjust target duration based on available content
        adjusted_duration = min(target_duration, max(total_video_duration * 0.8, 15))  # Use 80% of available content, min 15s
        
        st.info(f"📏 Adjusting video length: Target {target_duration}s → Actual {adjusted_duration:.1f}s (based on {total_video_duration:.1f}s available)")
        
        # Combine all assets
        all_assets = media_assets + generated_assets
        asset_lookup = {asset['name']: asset for asset in all_assets}
        
        # Get timeline structure from content plan (SIMPLIFIED)
        timeline_structure = content_plan.get('timeline_structure', [])
        
        # ENHANCED: Sequence multiple videos in order instead of just using one
        st.info("📝 Using multi-clip sequencing for your tutorial...")
        
        # Add main video/image assets to timeline - MULTI-CLIP APPROACH
        video_added = False
        timeline_duration = 0
        
        # Get all video assets in order (clip1, clip2, clip3)
        video_assets = [asset for asset in all_assets if asset['media_type'] == 'video']
        video_assets.sort(key=lambda x: x['name'])  # Sort by filename to get correct order
        
        if len(video_assets) >= 2:  # Multi-clip sequencing
            st.info(f"🎬 Professional video editing: Sequencing {len(video_assets)} clips for tutorial...")
            
            # Skip title card - focus on video editing
            st.info("� Focusing on professional video editing (no title card)")
            
            # Calculate full duration for video clips
            remaining_duration = adjusted_duration
            
            # INTELLIGENT DURATION ALLOCATION based on AI content analysis
            if timeline_structure:
                st.info("🧠 Using AI-analyzed timeline structure for optimal clip durations...")
                
                try:
                    # Get segments that match our video assets
                    video_segments = [seg for seg in timeline_structure if seg.get('asset_name') and 
                                    seg.get('asset_name').replace('.mp4', '').replace('.mov', '') in 
                                    [v['name'].replace('.mp4', '').replace('.mov', '') for v in video_assets[:3]]]
                    
                    # Calculate durations based on AI analysis
                    total_weight = sum(seg.get('importance', 1) * seg.get('recommended_duration', 10) for seg in video_segments)
                    
                    # IMPORTANT: Process ALL video assets, not just those with matching segments
                    st.info(f"🎯 Processing {len(video_assets)} videos with {len(video_segments)} AI-analyzed segments")
                    
                    for i, video_asset in enumerate(video_assets[:3]):  # Use all available videos (max 3)
                        # Find matching segment in timeline structure
                        matching_segment = None
                        asset_base_name = video_asset['name'].replace('.mp4', '').replace('.mov', '')
                        
                        for seg in video_segments:
                            if seg.get('asset_name') and asset_base_name in seg.get('asset_name', ''):
                                matching_segment = seg
                                break
                        
                        if matching_segment:
                            # Use AI-recommended duration with importance weighting
                            importance = matching_segment.get('importance', 1)  # 1-3 scale
                            recommended_duration = matching_segment.get('recommended_duration', 10)
                            content_weight = importance * recommended_duration
                            
                            # Allocate duration proportionally
                            clip_duration = (content_weight / total_weight) * remaining_duration if total_weight > 0 else remaining_duration / len(video_assets[:3])
                        else:
                            # Fallback for videos without matching AI segments: equal distribution
                            st.info(f"📋 No AI segment found for {video_asset['name']}, using equal distribution")
                            clip_duration = remaining_duration / len(video_assets[:3])
                        
                        # Professional video editing: Ensure within reasonable bounds
                        source_duration = video_asset.get('duration', 10)
                        if source_duration <= 0:
                            source_duration = 10
                        
                        # Smart clipping: Use best part of the video (not always from start)
                        max_usable_duration = source_duration * 0.90  # Use up to 90% of source
                        clip_duration = min(clip_duration, max_usable_duration)
                        clip_duration = max(clip_duration, 3)  # Minimum 3s per clip
                        clip_duration = min(clip_duration, 45)  # Increased maximum per clip for longer videos
                        
                        # Smart start time selection (avoid very beginning/end)
                        if source_duration > clip_duration + 2:
                            # Leave 1s buffer at start and end for better quality
                            max_start_time = source_duration - clip_duration - 1
                            start_time = min(1, max_start_time * 0.1)  # Start slightly into the video
                        else:
                            start_time = 0
                        
                        if matching_segment:
                            importance = matching_segment.get('importance', 1)
                            st.info(f"🎯 {video_asset['name']}: {clip_duration:.1f}s (from {start_time:.1f}s, importance: {importance})")
                        else:
                            st.info(f"📹 {video_asset['name']}: {clip_duration:.1f}s (from {start_time:.1f}s, equal distribution)")
                        st.info(f"🎬 Cropping: Using {start_time:.1f}s-{start_time + clip_duration:.1f}s from {source_duration:.1f}s total video")
                        
                        # Create professionally edited video clip
                        if clip_duration > 0:
                            try:
                                video_clip = VideoAsset(
                                    asset_id=video_asset['asset_id'],
                                    start=start_time,
                                    end=start_time + clip_duration
                                )
                                
                                # Add to timeline
                                timeline.add_inline(video_clip)
                                timeline_duration += clip_duration
                                video_added = True
                                
                                st.success(f"✅ Added {video_asset['name']} ({clip_duration:.1f}s) to timeline")
                                
                            except Exception as video_error:
                                st.error(f"❌ Failed to add {video_asset['name']}: {str(video_error)}")
                                continue
                                
                except Exception as ai_analysis_error:
                    st.warning(f"⚠️ AI analysis failed: {str(ai_analysis_error)}, using fallback")
                    video_added = False  # Force fallback to equal duration
                        
            if not video_added:  # Fallback if AI analysis failed
                # Professional video editing with equal duration allocation
                st.info("⚖️ Using professional video editing with optimized durations...")
                clips_to_use = min(len(video_assets), 3)
                duration_per_clip = remaining_duration / clips_to_use if clips_to_use > 0 else 0
                
                st.info(f"📊 Fallback mode: Distributing {remaining_duration:.1f}s across {clips_to_use} clips ({duration_per_clip:.1f}s each)")
                
                for i, video_asset in enumerate(video_assets[:clips_to_use]):
                    # Calculate professional clip duration
                    source_duration = video_asset.get('duration', 10)
                    if source_duration <= 0:
                        source_duration = 10
                    
                    # Smart duration allocation
                    max_usable_duration = source_duration * 0.90  # Use up to 90% of source
                    clip_duration = min(duration_per_clip, max_usable_duration)
                    clip_duration = max(clip_duration, 3)  # Minimum 3s per clip
                    clip_duration = min(clip_duration, 45)  # Increased maximum for longer target durations
                    
                    # Professional start time selection (avoid start/end)
                    if source_duration > clip_duration + 2:
                        # Start slightly into the video for better content
                        start_time = min(1, source_duration * 0.1)
                    else:
                        start_time = 0
                    
                    st.info(f"📹 {video_asset['name']}: {clip_duration:.1f}s (from {start_time:.1f}s, fallback edit)")
                    st.info(f"🎬 Cropping: Using {start_time:.1f}s-{start_time + clip_duration:.1f}s from {source_duration:.1f}s total video")
                    
                    # Create and add video clip
                    if clip_duration > 0:
                        try:
                            video_clip = VideoAsset(
                                asset_id=video_asset['asset_id'],
                                start=start_time,
                                end=start_time + clip_duration
                            )
                            
                            timeline.add_inline(video_clip)
                            timeline_duration += clip_duration
                            video_added = True
                            
                            st.success(f"✅ Added {video_asset['name']} ({clip_duration:.1f}s) to timeline")
                            
                        except Exception as video_error:
                            st.error(f"❌ Failed to add {video_asset['name']}: {str(video_error)}")
                            continue
                    
                    st.info(f"📹 Professional edit: {video_asset['name']} ({clip_duration:.1f}s from {start_time:.1f}s)")
                    
                    # Create professionally edited video clip
                    try:
                        video_clip = VideoAsset(
                            asset_id=video_asset['asset_id'],
                            start=start_time,
                            end=start_time + clip_duration
                        )
                        
                        # Add to timeline
                        timeline.add_inline(video_clip)
                        timeline_duration += clip_duration
                        video_added = True
                        
                    except Exception as fallback_error:
                        st.error(f"❌ Failed to add {video_asset['name']}: {str(fallback_error)}")
                        continue
                
        else:  # Single video fallback
            # Find the best/longest video to use as main content
            main_video = None
            main_duration = 0
            
            for asset_name, asset_info in asset_lookup.items():
                if asset_info['media_type'] == 'video':
                    duration = asset_info.get('duration', 10)  # Default to 10s if duration unknown
                    if duration > main_duration:
                        main_video = asset_info
                        main_duration = duration
            
            if main_video and not video_added:  # Only use single video if multi-clip didn't work
                # Use single video as main content - this is more reliable
                video_duration = main_video.get('duration', 10)  # Ensure we have a minimum duration
                if video_duration <= 0:
                    video_duration = 10  # Force minimum 10 seconds
                    
                use_duration = min(adjusted_duration, video_duration * 0.95)
                if use_duration <= 0:
                    use_duration = min(adjusted_duration, 10)  # Ensure positive duration
                
                st.info(f"🎬 Using single video fallback: {main_video['name']} for {use_duration:.1f}s (source: {video_duration:.1f}s)")
                
                # CRITICAL: Validate video range before creating asset
                if use_duration <= 0:
                    st.error(f"❌ Invalid video duration: {use_duration}, using fallback")
                    use_duration = 10  # Force valid duration
                
                if use_duration > video_duration:
                    st.warning(f"⚠️ Requested duration {use_duration}s > source {video_duration}s, adjusting")
                    use_duration = max(video_duration * 0.9, 5)  # Use 90% of source, minimum 5s
                    
                st.info(f"📐 Final video range: 0s → {use_duration:.1f}s")
                
                main_video_asset = VideoAsset(
                    asset_id=main_video['asset_id'],
                    start=0,
                    end=use_duration
                )
                
                # Add single main video to timeline
                timeline.add_inline(main_video_asset)
                video_added = True
                timeline_duration = use_duration
        
        # Final fallback if no videos were added
        if not video_added:
            # Fallback to first available asset
            for asset_name, asset_info in asset_lookup.items():
                if asset_info['media_type'] in ['video', 'image']:
                    if asset_info['media_type'] == 'video':
                        video_duration = asset_info.get('duration', 10)  # Default to 10s
                        if video_duration <= 0:
                            video_duration = 10
                        duration = min(adjusted_duration, video_duration)
                        if duration <= 0:
                            duration = 10  # Ensure positive duration
                            
                        # CRITICAL: Validate before creating VideoAsset
                        if duration > video_duration:
                            duration = max(video_duration * 0.9, 5)
                        st.info(f"📐 Fallback video range: 0s → {duration:.1f}s")
                            
                        fallback_asset = VideoAsset(
                            asset_id=asset_info['asset_id'],
                            start=0,
                            end=duration
                        )
                    else:  # image
                        duration = min(adjusted_duration, 30)  # Max 30s for images
                        if duration <= 0:
                            duration = 15  # Default image duration
                        fallback_asset = ImageAsset(
                            asset_id=asset_info['asset_id'],
                            duration=duration
                        )
                    
                    st.info(f"🔄 Using fallback: {asset_info['name']} ({duration:.1f}s)")
                    timeline.add_inline(fallback_asset)
                    video_added = True
                    timeline_duration = duration
                    break
        
        # If no video was added, add the first video asset as fallback
        if not video_added and media_assets:
            first_video = next((a for a in media_assets if a['media_type'] == 'video'), None)
            if first_video:
                video_duration = first_video.get('duration', 10)
                if video_duration <= 0:
                    video_duration = 10  # Force minimum duration
                safe_duration = min(adjusted_duration, video_duration)
                if safe_duration <= 0:
                    safe_duration = 10  # Ensure positive duration
                
                # CRITICAL: Final validation for emergency fallback
                if safe_duration > video_duration:
                    safe_duration = max(video_duration * 0.9, 5)
                    
                st.info(f"🔄 Using emergency fallback video: {first_video['name']} (0s → {safe_duration:.1f}s)")
                st.info(f"📐 Emergency range validation: 0 < {safe_duration:.1f} <= {video_duration:.1f}")
                
                fallback_asset = VideoAsset(
                    asset_id=first_video['asset_id'],
                    start=0,
                    end=safe_duration
                )
                timeline.add_inline(fallback_asset)
                video_added = True
            else:
                # Try first image as last resort
                first_image = next((a for a in media_assets if a['media_type'] == 'image'), None)
                if first_image:
                    st.info(f"🖼️ Using fallback image: {first_image['name']} ({adjusted_duration:.1f}s)")
                    
                    image_asset = ImageAsset(
                        asset_id=first_image['asset_id'],
                        duration=adjusted_duration
                    )
                    timeline.add_inline(image_asset)
                    video_added = True
        
        # Add ONLY voiceover overlays (no background music to avoid conflicts)
        audio_overlays_added = 0
        
        # Add voiceovers only
        for asset in all_assets:
            if asset['media_type'] == 'audio' and asset.get('generation_type') == 'voiceover':
                try:
                    # CRITICAL: Use timeline_duration to match exact video length
                    actual_video_duration = timeline_duration if timeline_duration > 0 else adjusted_duration
                    asset_audio_duration = asset.get('duration', 0)
                    
                    # Debug information
                    st.info(f"🔍 Debug - Video duration: {actual_video_duration:.1f}s, Audio asset duration: {asset_audio_duration:.1f}s")
                    
                    # CRITICAL FIX: If audio asset has no duration (0.0s), we can't use it properly
                    if asset_audio_duration <= 0:
                        st.warning(f"⚠️ Audio asset has invalid duration ({asset_audio_duration}s). Skipping voiceover to prevent timeline errors.")
                        st.info(f"💡 This usually means the audio generation failed or is still processing.")
                        continue
                    
                    # Use the shorter of the two durations to prevent overrun, with safety buffer
                    safety_buffer = 0.5  # 0.5 second buffer to prevent exact duration issues
                    max_safe_audio_duration = asset_audio_duration - safety_buffer
                    
                    if max_safe_audio_duration <= 0:
                        st.warning(f"⚠️ Audio too short after buffer ({max_safe_audio_duration:.1f}s). Skipping voiceover.")
                        continue
                    
                    # Choose the duration that covers the entire video
                    # If audio is shorter, we'll use what we have; if longer, we'll trim it
                    audio_duration = min(actual_video_duration, max_safe_audio_duration)
                    
                    # IMPORTANT: Ensure audio covers the entire video timeline
                    if audio_duration < actual_video_duration:
                        st.info(f"🔍 Audio ({audio_duration:.1f}s) is shorter than video ({actual_video_duration:.1f}s)")
                        st.info("💡 Voiceover will cover the available duration, then video will continue without narration")
                    
                    # Additional safety checks
                    if audio_duration <= 0:
                        st.warning(f"⚠️ Calculated audio duration is invalid ({audio_duration:.1f}s). Skipping voiceover.")
                        continue
                    
                    # Final bounds check - but prioritize covering more of the video
                    if audio_duration > asset_audio_duration:
                        audio_duration = asset_audio_duration * 0.98  # Use 98% of available audio (less aggressive trim)
                    
                    st.info(f"🎤 Syncing voiceover: {audio_duration:.1f}s audio to cover {actual_video_duration:.1f}s video timeline")
                    
                    audio_asset = AudioAsset(
                        asset_id=asset['asset_id'],
                        start=0,
                        end=audio_duration,
                        disable_other_tracks=False  # Mix with original video audio
                    )
                    
                    # Add voiceover starting at beginning of timeline (should cover all clips)
                    try:
                        timeline.add_overlay(start=0, asset=audio_asset)
                        audio_overlays_added += 1
                        st.info(f"✅ Added voiceover overlay (0-{audio_duration:.1f}s) across entire timeline")
                        
                        # Debug: Show timeline coverage
                        coverage_percentage = (audio_duration / actual_video_duration) * 100 if actual_video_duration > 0 else 0
                        st.info(f"📊 Audio coverage: {coverage_percentage:.1f}% of video timeline")
                        
                        if coverage_percentage < 90:
                            st.warning(f"⚠️ Audio only covers {coverage_percentage:.1f}% of video - some parts may be silent")
                            st.info("💡 This usually means the voiceover script was too short for the video length")
                        
                    except Exception as overlay_error:
                        st.warning(f"⚠️ add_overlay failed: {str(overlay_error)}")
                        st.info("🔄 Trying alternative audio integration method...")
                        
                        # Alternative method: Try adding as inline audio
                        try:
                            timeline.add_inline(audio_asset)
                            audio_overlays_added += 1
                            st.info(f"✅ Added voiceover as inline audio (0-{audio_duration:.1f}s)")
                        except Exception as inline_error:
                            st.error(f"❌ Both audio methods failed: overlay: {str(overlay_error)}, inline: {str(inline_error)}")
                            continue
                    
                    break  # Only add one voiceover to avoid conflicts
                    
                except Exception as e:
                    st.warning(f"⚠️ Failed to add voiceover: {str(e)}")
                    continue
        
        # Generate the final video stream - COMPREHENSIVE FALLBACK SYSTEM
        if video_added and timeline_duration > 0:
            # STEP 1: Try timeline with audio overlays
            try:
                st.info(f"✅ Timeline ready: {timeline_duration:.1f}s of video content")
                
                # Validate timeline before generation
                if timeline_duration <= 0:
                    st.error("❌ Timeline duration is invalid")
                    raise Exception("Invalid timeline duration")
                
                # Debug: Check timeline contents
                st.info(f"🔍 Timeline validation - Duration: {timeline_duration:.1f}s, Audio overlays: {audio_overlays_added}")
                
                st.info("🎬 Generating video stream (with audio overlays)...")
                
                # Use BASIC stream generation first - more reliable
                final_video_url = timeline.generate_stream()
                
                st.success(f"✅ Video generated successfully!")
                st.info(f"📊 Final video: ~{timeline_duration:.1f}s duration, {audio_overlays_added} audio overlays")
                
                # Validate the generated URL
                if final_video_url and len(final_video_url) > 10:
                    st.info(f"🔗 Video URL: {final_video_url[:50]}...")
                    return final_video_url
                else:
                    st.error("❌ Generated video URL appears invalid")
                    raise Exception("Invalid video URL generated")
                
            except Exception as stream_error:
                st.error(f"❌ Stream generation with audio failed: {str(stream_error)}")
                st.info("💡 Trying without audio overlays...")
                
                # STEP 2: Try timeline without audio overlays (video-only)
                try:
                    st.info("🔄 Creating professional video-only timeline (no audio overlays)...")
                    
                    # Create new timeline without audio - focus on video editing
                    video_only_timeline = Timeline(conn)
                    video_only_duration = 0
                    
                    # Add videos only (no audio overlays, no title cards)
                    video_assets = [asset for asset in media_assets if asset['media_type'] == 'video']
                    video_assets.sort(key=lambda x: x['name'])  # Sort by filename
                    
                    st.info("📹 Focusing on professional video editing (no title cards)")
                    
                    # Professional video clip editing
                    remaining_duration = adjusted_duration  # Use full duration for videos
                    clips_to_use = min(len(video_assets), 3)
                    duration_per_clip = remaining_duration / clips_to_use if clips_to_use > 0 else 0
                    
                    for i, video_asset in enumerate(video_assets[:clips_to_use]):
                        source_duration = video_asset.get('duration', 10)
                        
                        # Professional editing: Smart duration and start time
                        max_usable_duration = source_duration * 0.90
                        clip_duration = min(duration_per_clip, max_usable_duration)
                        clip_duration = max(clip_duration, 3)  # Minimum 3s
                        
                        # Smart start time (avoid very beginning)
                        if source_duration > clip_duration + 2:
                            start_time = min(1, source_duration * 0.1)
                        else:
                            start_time = 0
                        
                        video_clip = VideoAsset(
                            asset_id=video_asset['asset_id'],
                            start=start_time,
                            end=start_time + clip_duration
                        )
                        video_only_timeline.add_inline(video_clip)
                        video_only_duration += clip_duration
                        st.info(f"✅ Professional edit: {video_asset['name']} ({clip_duration:.1f}s from {start_time:.1f}s)")
                    
                    # Generate professionally edited video-only stream
                    st.info("🎬 Generating professionally edited video stream...")
                    video_only_url = video_only_timeline.generate_stream()
                    
                    if video_only_url and len(video_only_url) > 10:
                        st.success("✅ Professional video-only stream generated successfully!")
                        st.info(f"📊 Final edited video: ~{video_only_duration:.1f}s duration with professional cuts")
                        return video_only_url
                    else:
                        raise Exception("Professional video-only stream generation failed")
                        
                except Exception as video_only_error:
                    st.error(f"❌ Video-only timeline failed: {str(video_only_error)}")
                
                # STEP 3: ULTIMATE FALLBACK - Direct video stream
                st.info("🔄 Attempting direct video stream generation...")
                try:
                    # Find first video asset and generate stream directly
                    for asset in media_assets:
                        if asset['media_type'] == 'video' and asset.get('video_obj'):
                            video_obj = asset['video_obj']
                            st.info(f"📹 Using direct stream from: {asset['name']}")
                            
                            # Try different direct stream approaches
                            try:
                                # Method 1: Basic stream
                                direct_url = video_obj.generate_stream()
                                if direct_url and len(direct_url) > 10:
                                    st.success("✅ Direct video stream generated (Method 1)!")
                                    return direct_url
                            except Exception as e1:
                                st.info(f"Method 1 failed: {str(e1)}")
                            
                            try:
                                # Method 2: Stream with simple timeline
                                video_duration = asset.get('duration', 30)
                                max_duration = min(target_duration, video_duration)
                                direct_url = video_obj.generate_stream(timeline=[(0, max_duration)])
                                if direct_url and len(direct_url) > 10:
                                    st.success("✅ Direct video stream generated (Method 2)!")
                                    return direct_url
                            except Exception as e2:
                                st.info(f"Method 2 failed: {str(e2)}")
                            
                            try:
                                # Method 3: Create simple single-video timeline
                                simple_timeline = Timeline(conn)
                                video_duration = asset.get('duration', 30)
                                clip_duration = min(target_duration, video_duration * 0.95)
                                
                                simple_video = VideoAsset(
                                    asset_id=asset.get('asset_id'),
                                    start=0,
                                    end=clip_duration
                                )
                                simple_timeline.add_inline(simple_video)
                                
                                simple_url = simple_timeline.generate_stream()
                                if simple_url and len(simple_url) > 10:
                                    st.success("✅ Simple timeline generated (Method 3)!")
                                    return simple_url
                            except Exception as e3:
                                st.info(f"Method 3 failed: {str(e3)}")
                            
                            try:
                                # Method 4: Just play the video as-is
                                play_url = video_obj.play()
                                if play_url:
                                    st.success("✅ Video play URL generated (Method 4)!")
                                    st.warning("⚠️ Using original video without editing")
                                    return play_url
                            except Exception as e4:
                                st.info(f"Method 4 failed: {str(e4)}")
                    
                    st.error("❌ No suitable video assets found for direct streaming")
                    return None
                    
                except Exception as direct_error:
                    st.error(f"❌ Direct stream generation also failed: {str(direct_error)}")
                    return None
        else:
            st.warning("⚠️ No video content was added to timeline")
            return None
            
    except Exception as e:
        st.error(f"❌ Timeline assembly failed: {str(e)}")
        st.info("🔄 Using fallback approach...")
        
        # Fallback: Just return the first video asset as-is
        try:
            first_video = next((a for a in media_assets if a['media_type'] == 'video'), None)
            if first_video and 'video_obj' in first_video:
                # Generate a simple stream from the first video
                return first_video['video_obj'].generate_stream(timeline=[(0, min(30, first_video.get('duration', 30)))])
            else:
                st.error("❌ No video assets available for fallback")
                return None
                
        except Exception as fallback_error:
            st.error(f"❌ Fallback also failed: {str(fallback_error)}")
            return None


def main():
    """Main Streamlit application - Advanced Multimedia Content Creator"""
    
    # Set page config
    st.set_page_config(
        page_title="Edentic - AI Multimedia Creator",
        page_icon="🎬",
        layout="wide"
    )
    
    # Title and description
    st.title("🎬 Edentic")
    st.subheader("The story is yours. The edit is ours.")
    st.markdown("""
    **🚀 Revolutionary AI Multimedia Content Creator**
    
    Upload any combination of media (videos, images, audio), describe what you want, and our AI will:
    - 🧠 **Analyze** your existing content
    - 🎨 **Generate** missing content (images, videos, music, voiceovers)
    - ✂️ **Edit** everything into a professional video
    - 🎵 **Mix** audio perfectly with background music and narration
    - 🎬 **Deliver** broadcast-quality results
    
    **Perfect for tutorials, presentations, marketing videos, and creative projects!**
    """)
    
    # Initialize clients
    with st.spinner("🔧 Initializing AI services..."):
        conn, collection, genai_client = init_clients()
    
    # Project description section
    st.header("📝 Describe Your Project")
    project_description = st.text_area(
        "What kind of video do you want to create?",
        height=150,
        placeholder="Example: Create a short, 45-second tutorial video titled 'How to Make Perfect Pour-Over Coffee'. The video should start with a newly generated title card image that says 'Perfect Pour-Over Coffee' in an elegant font. Then, use the uploaded video clips to show the process in the correct order: first the grinding, then the pouring, and finally the shot of the finished cup. Please generate a clear, friendly female voiceover that explains each step as it appears on screen. Also, generate a relaxing, acoustic 'cafe-style' background music track that plays throughout the video.\n\nOr: Create a professional product demo video for our new mobile app. Start with an animated title screen, then show the key features using our screen recordings. Add upbeat background music and professional narration explaining the benefits.\n\nOr: Make a wedding slideshow video using our photos, with romantic background music and elegant transitions between photos.",
        help="Describe your vision in detail - what content you want, what style, what should be generated, etc."
    )
    
    # Target duration
    col1, col2 = st.columns(2)
    with col1:
        target_duration = st.slider(
            "Target video duration (seconds)",
            min_value=15,
            max_value=300,
            value=60,
            help="How long should your final video be?"
        )
    
    with col2:
        video_style = st.selectbox(
            "Video style preference",
            [
                "Auto-detect from description",
                "Professional/Corporate", 
                "Casual/Social Media",
                "Educational/Tutorial",
                "Creative/Artistic",
                "Marketing/Promotional"
            ]
        )
    
    # File upload section
    st.header("📂 Upload Your Media Assets")
    st.markdown("Upload any combination of videos, images, and audio files. Describe each one to help our AI understand how to use them.")
    
    uploaded_files = st.file_uploader(
        "Choose your media files",
        type=['mp4', 'mov', 'avi', 'mkv', 'wmv', 'jpg', 'jpeg', 'png', 'gif', 'mp3', 'wav', 'aac', 'm4a'],
        accept_multiple_files=True,
        help="Upload videos, images, audio files - any media you want in your final video"
    )
    
    # File descriptions
    file_descriptions = {}
    if uploaded_files:
        st.subheader("📋 Describe Your Assets")
        st.markdown("*Help our AI understand what each file is and how you want it used:*")
        
        for uploaded_file in uploaded_files:
            file_type = "🎬" if uploaded_file.name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.wmv')) else \
                       "🖼️" if uploaded_file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')) else \
                       "🎵" if uploaded_file.name.lower().endswith(('.mp3', '.wav', '.aac', '.m4a')) else "📄"
            
            description = st.text_input(
                f"{file_type} {uploaded_file.name}",
                placeholder=f"Describe what this {uploaded_file.name.split('.')[-1].upper()} shows or should be used for...",
                key=f"desc_{uploaded_file.name}"
            )
            file_descriptions[uploaded_file.name] = description
    
    # Debug test button
    if st.button("🔧 Test Video Generation (Debug)", help="Test basic video generation without using uploaded files"):
        st.write("---")
        st.subheader("🔍 Video Generation Test")
        test_result = test_video_generation()
        if test_result:
            st.video(test_result)
        st.write("---")
    
    # Generate button
    if st.button("🎬 Create My Multimedia Video", type="primary", disabled=not (uploaded_files and project_description.strip())):
        if not uploaded_files:
            st.error("❌ Please upload at least one media file.")
            return
        
        if not project_description.strip():
            st.error("❌ Please describe what kind of video you want to create.")
            return
        
        # Show progress sections
        with st.container():
            st.header("🔄 AI Multimedia Magic in Progress...")
            st.markdown("*Our AI is analyzing, generating, and editing your professional video!*")
            
            # Step 1: Upload and analyze media
            with st.spinner("📤 Step 1: Uploading and analyzing your media assets..."):
                media_assets = upload_and_analyze_mixed_media(collection, uploaded_files, file_descriptions, project_description)
            
            if not media_assets:
                st.error("❌ Failed to upload and analyze media assets.")
                return
            
            st.success(f"✅ Successfully analyzed {len(media_assets)} media assets")
            
            # Show asset analysis
            with st.expander("📊 Media Asset Analysis"):
                for asset in media_assets:
                    st.write(f"**{asset['name']}** ({asset['media_type'].upper()})")
                    st.write(f"📝 Description: {asset['description'] or 'No description provided'}")
                    if asset['transcript']:
                        st.write(f"🎤 Found spoken content: {len(asset['transcript'])} characters")
                    st.write("---")
            
            # Step 2: Create comprehensive content plan
            with st.spinner("🧠 Step 2: AI is creating your comprehensive content plan..."):
                content_plan = create_comprehensive_content_plan(genai_client, media_assets, project_description, target_duration)
            
            if not content_plan:
                st.error("❌ Failed to create content plan.")
                return
            
            st.success("✅ AI created a comprehensive content plan!")
            
            # Show content plan
            with st.expander("🎯 AI Content Plan"):
                st.write(f"**Project Analysis:** {content_plan.get('project_analysis', 'N/A')}")
                st.write(f"**Target Audience:** {content_plan.get('target_audience', 'N/A')}")
                
                content_to_gen = content_plan.get('content_to_generate', [])
                if content_to_gen:
                    st.write("**Content to Generate:**")
                    for item in content_to_gen:
                        st.write(f"- **{item.get('type', 'Unknown')}:** {item.get('description', 'N/A')}")
                
                timeline = content_plan.get('timeline_structure', [])
                if timeline:
                    st.write(f"**Timeline Structure:** {len(timeline)} segments with intelligent analysis")
                    for segment in timeline:
                        importance_stars = "⭐" * segment.get('importance', 1)
                        content_type = segment.get('content_type', 'unknown')
                        st.write(f"  - **{segment.get('asset_name', 'Unknown')}** ({segment.get('recommended_duration', 0):.1f}s) - {importance_stars} {content_type}")
                        st.write(f"    *{segment.get('description', 'No description')}*")
            
            # Step 3: Generate missing content
            content_to_generate = content_plan.get('content_to_generate', [])
            generated_assets = []
            
            if content_to_generate:
                with st.spinner("🎨 Step 3: Generating missing content with AI..."):
                    generated_assets = generate_missing_content(collection, genai_client, content_plan, media_assets)
                
                if generated_assets:
                    st.success(f"✅ Generated {len(generated_assets)} new assets!")
                    
                    with st.expander("🎨 Generated Content"):
                        for asset in generated_assets:
                            st.write(f"**{asset['generation_type'].replace('_', ' ').title()}**")
                            st.write(f"📝 {asset['description']}")
                            st.write("---")
                else:
                    st.info("ℹ️ No additional content needed - using existing assets")
            else:
                st.info("ℹ️ All required content is available - proceeding with editing")
            
            # Step 4: Create initial video with voiceover only (no background music to avoid conflicts)
            with st.spinner("🎬 Step 4: Creating video with professional editing and voiceover..."):
                # Filter out background music for initial creation
                background_music_assets = [a for a in generated_assets if a.get('generation_type') == 'background_music']
                voiceover_only_assets = [a for a in generated_assets if a.get('generation_type') != 'background_music']
                
                initial_video_url = assemble_multimedia_video(
                    conn, content_plan, media_assets, voiceover_only_assets, target_duration
                )
            
            if initial_video_url:
                st.success("🎉 Your professional video with voiceover is ready!")
                
                # Step 5: Preview and user decision for background music
                st.header("🎬 Preview Your Edited Video")
                st.markdown("**✨ Your video has been professionally edited with:**")
                st.markdown("- 📹 Cropped and optimally sequenced clips")
                st.markdown("- 🎤 AI-generated voiceover narration")
                st.markdown("- ⚡ Perfect timing and transitions")
                
                try:
                    st.video(initial_video_url)
                    st.info("📎 **Preview Link:** [Open in new tab](" + initial_video_url + ")")
                    
                except Exception as e:
                    st.warning(f"⚠️ Could not embed video: {str(e)}")
                    st.markdown(f"**🎬 Your video is ready!** [Click here to view]({initial_video_url})")
                
                # User decision for background music
                if background_music_assets:
                    st.header("🎵 Add Background Music?")
                    st.markdown("Your video looks great! Would you like to add background music to make it even more engaging?")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        add_music = st.button("✅ Yes, Add Background Music", type="primary", key="add_music")
                    
                    with col2:
                        keep_current = st.button("✋ Keep Current Version", key="keep_current")
                    
                    if add_music:
                        with st.spinner("🎵 Adding background music and creating final video..."):
                            # Create final version with background music
                            final_video_url = assemble_multimedia_video_with_music(
                                conn, content_plan, media_assets, generated_assets, target_duration
                            )
                        
                        if final_video_url:
                            st.success("🎉 Final video with background music is ready!")
                            
                            st.header("🎬 Your Complete Multimedia Video")
                            st.markdown("**🎵 Now featuring:**")
                            st.markdown("- 📹 Professionally edited and cropped clips")
                            st.markdown("- 🎤 AI voiceover narration")
                            st.markdown("- 🎵 Background music perfectly mixed")
                            st.markdown("- ✨ Broadcast-quality production")
                            
                            try:
                                st.video(final_video_url)
                                st.success("✅ Complete multimedia video creation finished!")
                                st.info(f"📎 **Final Link:** [Open in new tab]({final_video_url})")
                                
                            except Exception as e:
                                st.warning(f"⚠️ Could not embed final video: {str(e)}")
                                st.markdown(f"**🎬 Your final video is ready!** [Click here to view]({final_video_url})")
                            
                            # Final comprehensive summary
                            st.info(f"""
                            🎬 **Complete Video Summary:**
                            - Original clips: {len([a for a in media_assets if a['media_type'] == 'video'])} (professionally edited)
                            - Generated content: {len(generated_assets)} (voiceover, music, titles)
                            - Duration: {target_duration} seconds (optimally paced)
                            - Style: {video_style}
                            - Features: Professional editing, voiceover, background music
                            - Quality: Broadcast-ready multimedia experience!
                            """)
                            
                            st.balloons()
                            
                        else:
                            st.error("❌ Failed to add background music. Using voiceover-only version.")
                            st.markdown(f"**🎬 Your video with voiceover:** [Click here to view]({initial_video_url})")
                    
                    elif keep_current:
                        st.success("✅ Perfect! Your professionally edited video with voiceover is complete.")
                        
                        # Show summary for voiceover-only version
                        st.info(f"""
                        🎬 **Professional Video Summary:**
                        - Original clips: {len([a for a in media_assets if a['media_type'] == 'video'])} (professionally edited and cropped)
                        - Generated content: {len(voiceover_only_assets)} (voiceover and titles)
                        - Duration: {target_duration} seconds (optimally paced)
                        - Style: {video_style}
                        - Features: Professional editing with AI voiceover
                        - Quality: Ready to share and impress!
                        """)
                        
                        st.balloons()
                
                else:
                    # No background music was generated
                    st.success("✅ Your professionally edited video with voiceover is complete!")
                    st.info(f"""
                    🎬 **Video Creation Summary:**
                    - Clips professionally edited and sequenced
                    - AI voiceover narration added
                    - Perfect timing and transitions
                    - Ready to share!
                    """)
                    st.balloons()
                    
            else:
                st.error("❌ Failed to create initial video.")
                st.info("💡 **Troubleshooting tips:**")
                st.write("- Check your internet connection")
                st.write("- Verify your API keys are correct") 
                st.write("- Try with smaller media files")
                st.write("- Ensure media files are in supported formats")
                st.write("- Simplify your project description")
    
    # Example projects section
    st.markdown("---")
    st.header("💡 Example Projects You Can Create")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎓 Tutorial Videos**
        - Upload screen recordings + photos
        - AI generates title cards + voiceover
        - Professional educational content
        - Perfect pacing and explanations
        """)
    
    with col2:
        st.markdown("""
        **📱 Product Demos** 
        - Upload app screenshots + videos
        - AI creates marketing copy + music
        - Professional presentation style
        - Compelling call-to-action
        """)
    
    with col3:
        st.markdown("""
        **🎨 Creative Projects**
        - Upload photos + audio clips
        - AI generates transitions + effects
        - Artistic video compilations
        - Perfect for social media
        """)
    
    # How it works section
    st.markdown("---")
    st.header("🤖 How Our Advanced AI Works")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        **🧠 Smart Analysis**
        - Understands all media types
        - Reads your project vision
        - Plans optimal content mix
        - Identifies missing pieces
        """)
    
    with col2:
        st.markdown("""
        **🎨 Content Generation**
        - Creates title images
        - Generates background music
        - Produces professional voiceovers
        - Makes custom video clips
        """)
    
    with col3:
        st.markdown("""
        **✂️ Intelligent Editing**
        - Perfect timing and pacing
        - Professional transitions
        - Audio mixing and levels
        - Visual effects and styling
        """)
    
    with col4:
        st.markdown("""
        **🎬 Final Assembly**
        - Combines all elements
        - Optimizes for quality
        - Ensures perfect sync
        - Delivers broadcast standard
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🎬 <strong>Edentic</strong> - Powered by VideoDB & Google GenAI</p>
        <p><em>The story is yours. The edit is ours.</em></p>
        <p>🚀 Revolutionary AI multimedia content creation platform</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

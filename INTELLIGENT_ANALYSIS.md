# Intelligent Content Analysis & Duration Allocation

## 🧠 **AI-Powered Clip Analysis**

The system now analyzes each clip's content description and intelligently allocates duration based on:

### **Content Importance (1-3 ⭐ scale)**
- **3 ⭐ High**: Keywords like "main", "key", "important", "focus", "primary", "central"  
- **2 ⭐ Medium**: Keywords like "process", "action", "making", "pouring", "grinding", "brewing"
- **1 ⭐ Standard**: Default for other content

### **Content Type Classification**
- **Process**: Grinding, making, preparation activities
- **Action**: Pouring, technique demonstrations  
- **Result**: Final shots, finished products

### **Smart Duration Recommendations**
- **Grinding/Process**: 1.2x base duration (up to 15s) - More time for complex processes
- **Pouring/Action**: 1.5x base duration (up to 18s) - Longer for key technique demonstrations
- **Final/Result**: 0.8x base duration (up to 10s) - Shorter for outcome shots

## 🎯 **Your Coffee Tutorial Analysis**

Based on your descriptions:

### **clip1.mp4**: "Close-up shot of coffee beans being ground"
- **Content Type**: Process
- **Importance**: 2 ⭐ (contains "grinding", "process")
- **Recommended Duration**: ~15s (extended for process complexity)

### **clip2.mp4**: "Hot water being carefully poured over grounds"  
- **Content Type**: Action
- **Importance**: 2 ⭐ (contains "pouring", "action")
- **Recommended Duration**: ~18s (extended for key technique)

### **clip3.mp4**: "Final shot of steaming, freshly brewed cup"
- **Content Type**: Result  
- **Importance**: 1 ⭐ (result/final shot)
- **Recommended Duration**: ~10s (shorter for outcome)

## 🎬 **Expected Timeline**

```
🖼️ Title Card: "Perfect Pour-Over Coffee" (3s)
📹 Grinding Process: clip1.mp4 (~15s) ⭐⭐
📹 Pouring Technique: clip2.mp4 (~18s) ⭐⭐  
📹 Final Result: clip3.mp4 (~9s) ⭐
🎤 Voiceover: Synchronized to 45s total
🎵 Background Music: Cafe-style throughout
```

**Total**: 45 seconds with intelligent content-based allocation instead of equal 15s splits!

## 🔍 **UI Display Enhancement**

The content plan now shows:
```
Timeline Structure: 3 segments with intelligent analysis
- clip1.mp4 (15.0s) - ⭐⭐ process
  A close-up shot of coffee beans being ground in a coffee grinder.
- clip2.mp4 (18.0s) - ⭐⭐ action  
  A shot of hot water being carefully poured over coffee grounds.
- clip3.mp4 (9.0s) - ⭐ result
  A final shot of a steaming, freshly brewed cup of black coffee.
```

The system now creates a more natural, content-aware video flow instead of mechanical equal splits!

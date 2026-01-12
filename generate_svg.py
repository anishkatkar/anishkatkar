import base64

# Configuration
IMAGE_PATH = "banner_bg.jpg"
FONT_PATH = "/Users/anishk/Downloads/swirly_canalope/SwirlyCanalope_PERSONAL_USE_ONLY.otf"
OUTPUT_PATH = "banner.svg"
FINAL_NAME = "Anish"

# Read and encode image
with open(IMAGE_PATH, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

# Read and encode font
with open(FONT_PATH, "rb") as font_file:
    encoded_font = base64.b64encode(font_file.read()).decode("utf-8")

# Animation Settings
words = ["hello", "hola", "bonjour", "namaste", "guten tag", "ciao"]
final_word = FINAL_NAME
step_duration = 2
total_intro_duration = len(words) * step_duration
final_hold_start = total_intro_duration

svg_content = f"""<svg width="800" height="400" viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <!-- Blur Filter -->
    <filter id="glassBlur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="15" />
    </filter>

    <!-- Fonts -->
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Pacifico&amp;display=swap');
      @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@700&amp;display=swap');
      
      @font-face {{
        font-family: 'Swirly Canalope';
        src: url(data:font/otf;charset=utf-8;base64,{encoded_font}) format('opentype');
      }}

      .hello-text {{
        font-family: 'Pacifico', cursive;
        font-size: 80px;
        fill: rgba(255, 255, 255, 0.9);
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        opacity: 0;
      }}
      
      .final-text {{
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 90px;
        fill: rgba(255, 255, 255, 1);
        text-shadow: 0 4px 25px rgba(0,0,0,0.4);
        opacity: 0;
        animation: finalize {0.5}s ease-out forwards;
        animation-delay: {final_hold_start}s;
      }}
      
      .subtitle {{
        font-family: 'Swirly Canalope', cursive;
        font-weight: normal;
        font-size: 50px; /* Increased for readability */
        fill: rgba(255, 255, 255, 0.9);
        letter-spacing: 2px;
        opacity: 0;
        /* Animation: Fade up + slight rotation or wobble for swishy effect? Just fade up for now to be safe */
        animation: finalizeSubtitle {0.8}s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        animation-delay: {final_hold_start + 0.3}s;
      }}

      @keyframes fadeCycle {{
        0% {{ opacity: 0; transform: scale(0.9); }}
        20% {{ opacity: 1; transform: scale(1); }}
        80% {{ opacity: 1; transform: scale(1); }}
        100% {{ opacity: 0; transform: scale(1.1); }}
      }}
      
      @keyframes finalize {{
        from {{ opacity: 0; transform: translateY(30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
      }}
      
      @keyframes finalizeSubtitle {{
        from {{ opacity: 0; transform: translateY(20px) scale(0.9); }}
        to {{ opacity: 1; transform: translateY(0) scale(1); }}
      }}

    </style>

    <!-- Animated Patterns -->
    <pattern id="bgPattern" patternUnits="userSpaceOnUse" width="1000" height="1000">
      <image href="data:image/jpeg;base64,{encoded_image}" x="0" y="0" width="1000" height="600" preserveAspectRatio="xMidYMid slice" />
      <animateTransform attributeName="patternTransform" type="translate" from="0 0" to="-100 -50" dur="30s" repeatCount="indefinite" additive="sum" />
      <animateTransform attributeName="patternTransform" type="scale" values="1; 1.1; 1" dur="30s" repeatCount="indefinite" additive="sum" />
    </pattern>
    
    <!-- Clip Path for the Card - Adjusted Size -->
    <!-- Increased height from 200 to 280 to fit bigger subtitle. Centered vertically. -->
    <rect id="cardShape" x="125" y="60" width="550" height="280" rx="30" ry="30" />
  </defs>

  <!-- Background -->
  <rect width="100%" height="100%" fill="url(#bgPattern)" />

  <!-- Glass Card -->
  <g>
    <g clip-path="url(#cardClip)">
        <clipPath id="cardClip">
            <use href="#cardShape" />
        </clipPath>
        <rect x="-50" y="-50" width="900" height="600" fill="url(#bgPattern)" filter="url(#glassBlur)" /> 
    </g>
    
    <use href="#cardShape" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.2)" stroke-width="1.5" />
    
    <!-- Greetings Cycle -->
"""

# Append greeting words
for i, word in enumerate(words):
    delay = i * step_duration
    # Centered in the new card height (approx y=200 is center of 400px canvas)
    svg_content += f'    <text x="400" y="200" text-anchor="middle" class="hello-text" style="animation: fadeCycle {step_duration}s ease-in-out {delay}s 1 forwards;">{word}</text>\n'

# Append Final Name and Subtitle
# Adjusting Y positions for the stacked text
svg_content += f"""
    <!-- Final Name -->
    <text x="400" y="180" text-anchor="middle" class="final-text" dominant-baseline="middle">{final_word}</text>
    <text x="400" y="260" text-anchor="middle" class="subtitle">Welcomes You</text>
  </g>
  
  <rect width="100%" height="100%" fill="rgba(0,0,0,0.1)" pointer-events="none" />
</svg>
"""

with open(OUTPUT_PATH, "w") as f:
    f.write(svg_content)
    
print(f"Generated {OUTPUT_PATH} with custom font.")

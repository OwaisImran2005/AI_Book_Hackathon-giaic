# Video Embedding Instructions

This document provides instructions on how to embed video demonstrations into the Docusaurus documentation. This task is to be completed after the video demonstrations have been recorded and edited (Task T085) and are available in the `static/videos/` directory.

## How to Embed Videos in Markdown/MDX

Docusaurus supports embedding videos using standard HTML5 `<video>` tags or by leveraging MDX capabilities.

### Using HTML5 `<video>` Tag

For simple embedding, you can use the `<video>` tag directly in your Markdown or MDX file:

```html
<video controls src="/videos/my_capstone_demo.mp4" width="640" height="360" muted autoplay loop>
  Your browser does not support the video tag.
</video>
```

**Explanation of attributes:**
-   `controls`: Displays video controls (play/pause, volume, fullscreen).
-   `src`: The path to your video file. This should be relative to your `static/` directory in Docusaurus (e.g., `/videos/my_capstone_demo.mp4` refers to `static/videos/my_capstone_demo.mp4`).
-   `width`, `height`: Sets the dimensions of the video player.
-   `muted`: Mutes the audio by default.
-   `autoplay`: Starts playing the video automatically.
-   `loop`: Loops the video continuously.

### Using MDX with a Custom Component (Advanced)

For more sophisticated video embedding with custom styling or additional features, you can create a reusable React component and use it in your MDX files.

**1. Create a React Component (e.g., `src/components/VideoPlayer.tsx`):**
```typescript jsx
import React from 'react';

interface VideoPlayerProps {
  src: string;
  title: string;
  width?: string;
  height?: string;
  autoplay?: boolean;
  loop?: boolean;
  muted?: boolean;
}

export default function VideoPlayer({
  src,
  title,
  width = '100%',
  height = 'auto',
  autoplay = false,
  loop = false,
  muted = false,
}: VideoPlayerProps): JSX.Element {
  return (
    <div style={{ margin: '20px 0' }}>
      <p style={{ fontWeight: 'bold' }}>{title}</p>
      <video controls src={src} width={width} height={height} autoPlay={autoplay} loop={loop} muted={muted} style={{ maxWidth: '100%' }}>
        Your browser does not support the video tag.
      </video>
    </div>
  );
}
```

**2. Use the Custom Component in your MDX file:**
```mdx
import VideoPlayer from '@site/src/components/VideoPlayer';

# My Chapter with Video

Here is an important video demonstration:

<VideoPlayer src="/videos/my_capstone_demo.mp4" title="Capstone Project Overview" autoplay muted loop />

This video illustrates the key concepts discussed above.
```

## Relevant Chapters for Video Embedding

Video demonstrations should primarily be embedded in the following chapters (once videos are available):

-   **Chapter 13: Capstone: Autonomous Humanoid**: For the main capstone project demonstration.
-   **Module Project sections**: In the `index.md` files for each module, a preview video of the module's project could be embedded.
-   Other relevant chapters where a visual demonstration significantly enhances understanding.

*(This is a manual task that requires human intervention to edit the specific Markdown/MDX files.)*

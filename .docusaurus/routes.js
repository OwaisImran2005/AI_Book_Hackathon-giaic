import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/blog',
    component: ComponentCreator('/blog', 'b2f'),
    exact: true
  },
  {
    path: '/blog/archive',
    component: ComponentCreator('/blog/archive', '182'),
    exact: true
  },
  {
    path: '/blog/authors',
    component: ComponentCreator('/blog/authors', '0b7'),
    exact: true
  },
  {
    path: '/blog/authors/all-sebastien-lorber-articles',
    component: ComponentCreator('/blog/authors/all-sebastien-lorber-articles', '4a1'),
    exact: true
  },
  {
    path: '/blog/authors/yangshun',
    component: ComponentCreator('/blog/authors/yangshun', 'a68'),
    exact: true
  },
  {
    path: '/blog/first-blog-post',
    component: ComponentCreator('/blog/first-blog-post', '89a'),
    exact: true
  },
  {
    path: '/blog/long-blog-post',
    component: ComponentCreator('/blog/long-blog-post', '9ad'),
    exact: true
  },
  {
    path: '/blog/mdx-blog-post',
    component: ComponentCreator('/blog/mdx-blog-post', 'e9f'),
    exact: true
  },
  {
    path: '/blog/tags',
    component: ComponentCreator('/blog/tags', '287'),
    exact: true
  },
  {
    path: '/blog/tags/docusaurus',
    component: ComponentCreator('/blog/tags/docusaurus', '704'),
    exact: true
  },
  {
    path: '/blog/tags/facebook',
    component: ComponentCreator('/blog/tags/facebook', '858'),
    exact: true
  },
  {
    path: '/blog/tags/hello',
    component: ComponentCreator('/blog/tags/hello', '299'),
    exact: true
  },
  {
    path: '/blog/tags/hola',
    component: ComponentCreator('/blog/tags/hola', '00d'),
    exact: true
  },
  {
    path: '/blog/welcome',
    component: ComponentCreator('/blog/welcome', 'd2b'),
    exact: true
  },
  {
    path: '/markdown-page',
    component: ComponentCreator('/markdown-page', '3d7'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'acb'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', 'c4d'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', 'ee1'),
            routes: [
              {
                path: '/docs/ai-robot-brain/',
                component: ComponentCreator('/docs/ai-robot-brain/', '8f7'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/ai-robot-brain/isaac-ros-perception',
                component: ComponentCreator('/docs/ai-robot-brain/isaac-ros-perception', 'bce'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/ai-robot-brain/nav2-path-planning',
                component: ComponentCreator('/docs/ai-robot-brain/nav2-path-planning', '6bf'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/ai-robot-brain/nvidia-isaac-sim',
                component: ComponentCreator('/docs/ai-robot-brain/nvidia-isaac-sim', 'ff2'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/appendices/cloud-setup',
                component: ComponentCreator('/docs/appendices/cloud-setup', '468'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/appendices/hardware-guide',
                component: ComponentCreator('/docs/appendices/hardware-guide', '433'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/appendices/resources',
                component: ComponentCreator('/docs/appendices/resources', '3ad'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/appendices/troubleshooting',
                component: ComponentCreator('/docs/appendices/troubleshooting', '430'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/digital-twin/',
                component: ComponentCreator('/docs/digital-twin/', 'd01'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/digital-twin/gazebo-fundamentals',
                component: ComponentCreator('/docs/digital-twin/gazebo-fundamentals', '4c3'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/digital-twin/physics-simulation',
                component: ComponentCreator('/docs/digital-twin/physics-simulation', '276'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/digital-twin/unity-integration',
                component: ComponentCreator('/docs/digital-twin/unity-integration', '13f'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/glossary',
                component: ComponentCreator('/docs/glossary', '552'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/instructor-guide',
                component: ComponentCreator('/docs/instructor-guide', '100'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', '38d'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/robotic-nervous-system/',
                component: ComponentCreator('/docs/robotic-nervous-system/', '47d'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/robotic-nervous-system/introduction-physical-ai',
                component: ComponentCreator('/docs/robotic-nervous-system/introduction-physical-ai', '1ae'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/robotic-nervous-system/ros2-architecture',
                component: ComponentCreator('/docs/robotic-nervous-system/ros2-architecture', '2e6'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/robotic-nervous-system/ros2-python-development',
                component: ComponentCreator('/docs/robotic-nervous-system/ros2-python-development', '965'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/robotic-nervous-system/urdf-robot-modeling',
                component: ComponentCreator('/docs/robotic-nervous-system/urdf-robot-modeling', '3c9'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/student-resources/ros2_python_cheat_sheet',
                component: ComponentCreator('/docs/student-resources/ros2_python_cheat_sheet', '333'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/student-resources/vla_reference_card',
                component: ComponentCreator('/docs/student-resources/vla_reference_card', '1b0'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/tutorial-basics/congratulations',
                component: ComponentCreator('/docs/tutorial-basics/congratulations', '70e'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-blog-post',
                component: ComponentCreator('/docs/tutorial-basics/create-a-blog-post', '315'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-document',
                component: ComponentCreator('/docs/tutorial-basics/create-a-document', 'f86'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-page',
                component: ComponentCreator('/docs/tutorial-basics/create-a-page', '9f6'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/deploy-your-site',
                component: ComponentCreator('/docs/tutorial-basics/deploy-your-site', 'b91'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/markdown-features',
                component: ComponentCreator('/docs/tutorial-basics/markdown-features', '272'),
                exact: true
              },
              {
                path: '/docs/tutorial-extras/manage-docs-versions',
                component: ComponentCreator('/docs/tutorial-extras/manage-docs-versions', 'a34'),
                exact: true
              },
              {
                path: '/docs/tutorial-extras/translate-your-site',
                component: ComponentCreator('/docs/tutorial-extras/translate-your-site', '739'),
                exact: true
              },
              {
                path: '/docs/video_embedding_instructions',
                component: ComponentCreator('/docs/video_embedding_instructions', 'b09'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/vision-language-action/',
                component: ComponentCreator('/docs/vision-language-action/', '663'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/vision-language-action/capstone-autonomous-humanoid',
                component: ComponentCreator('/docs/vision-language-action/capstone-autonomous-humanoid', 'a55'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/vision-language-action/llm-cognitive-planning',
                component: ComponentCreator('/docs/vision-language-action/llm-cognitive-planning', '281'),
                exact: true,
                sidebar: "mainSidebar"
              },
              {
                path: '/docs/vision-language-action/voice-to-action',
                component: ComponentCreator('/docs/vision-language-action/voice-to-action', '796'),
                exact: true,
                sidebar: "mainSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', 'e5f'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];

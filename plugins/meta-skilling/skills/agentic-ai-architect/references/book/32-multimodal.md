---
chapter: 32
title: "Multimodal"
part: "X — Everything Else"
source_pdf_pages: "113-117"
---

# Chapter 32: Multimodal
*Part X: Everything Else*

One way to think about multimodality (images, video, voice) in AI is to map their dates of origin on various platforms.

Consider the Internet: it supported text from its origin in the 1970s, but images and video weren't supported until the web browser (1992), and voice not until 1995.

Voice and video didn't become popular until Skype (2003) and YouTube (2005), with greater bandwidth and connection speeds.

Or think about social networks: all the early ones, like MySpace (2002), Facebook (2004), and Twitter (2008), were primarily text-based.

Image-based social media didn't become popular until Instagram (2010) and Snapchat (2013), and video-based social media until TikTok (2017).

In AI, then, it's little wonder that multi-modal use-cases are a bit younger and less mature. Like on earlier platforms, they're trickier to get right, and more computationally complex.

## Image Generation

March 2025 brought the invention of Ghibli-core —think soft colors, dreamy backgrounds, and those iconic wide-eyed characters.

People had been playing with Midjourney, Stable Diffusion, and others for a while. Transposing photos into specific styles with a single prompt, though, was a significant leap forward in consumer-grade image-generation.

People uploaded selfies or old photos, added a prompt, and instantly got back an anime version that looked straight out of "Spirited Away."

![The Mastra cofounders (Shane, Abhi and Sam) at a basketball game](image)

*The Mastra cofounders (Shane, Abhi and Sam) at a basketball game*

This wasn't just a niche thing: the Ghibli trend took over social feeds everywhere. The official (Trump) White House account joined the fray by (controversially) tweeting out a Ghibli-fied picture of a detained immigrant.

More broadly, the Ghibli moment showed vitality for the digital art use case — image gen for what was something that is a confluence between storyboard, a character sketch, and environment concepts.

## Use Cases

In terms of people using image gen for products, there are a few use-cases.

In marketing and e-commerce, product mockups on varied backgrounds and rapid ad creative generation without photoshoots and in various form factors. "Try-on" image models allow people to swap out the human model but keep the featured clothing item.

The third use-case for image gen has been in video game and film production. Image gen has allowed for asset prototyping, including portraits, textures, and props, as well as scene layout planning via rough "sketch to render" flows.

Put in web development terms, this gives the fidelity of a full design with the effort/skill of a wireframe.

Last, there are more NSFW use-cases. These don't tend to be venture-fundable, but at least according to the Silicon Valley gossip mills, quite a few of the more risqué use-cases print money — if you can find a payment processor that will take your business.

## Voice

The key modalities in voice are speech-to-text (STT), text-to-speech (TTS), and speech-to-speech, also known as realtime voice.

Most voice agents built in 2024 and early-to-mid 2025 used a speech-to-text (STT) and text-to-speech (TTS) pipeline. They use one model to translate input voice to text, another model to generate text and answer, and then translate the response text into an audio response.

Mastra offers some voice capabilities for agents. Here's an example of listening; you could follow this up with `agent.speak()` to reply.

```ts
import { Agent } from "@mastra/core/agent";
import { OpenAIVoice } from "@mastra/voice-openai";

const agent = new Agent({
  name: 'Agent',
  instructions: `You are a helpful assistant with voice capabilities.`,
  model: openai('gpt-4o'),
  voice: new OpenAIVoice(),
});

const audioStream =
  fs.createReadStream('/path/to.mp3')

const text = await agent.listen(audioStream)

// Hey! How are ya!
```

But capabilities are evolving quickly; end-to-end speech-to-speech models like OpenAI's `gpt-realtime` are increasingly deployed in production systems.

In order to do that, you could train a model that specifically takes voice tokens as input, and responds with voice tokens as output. That's known as "realtime voice", but it's proved challenging.

For one thing, it's difficult to train such models: the information density of audio is only 1/1000 of text, so these models take significantly more input data to train and cost more to serve.

Second, these models still struggle with turn-taking, known in the industry as "voice activity detection". When talking, humans interrupt each other constantly using both visual and emotional cues.

But voice models don't have these cues, and have to deal with both computational and network latency. When they interrupt too early, they cut people off; when they interrupt too late, they sound robotic.

While these products make great demos, there are not too many companies using realtime voice in production.

## Video

For most of 2025, we were waiting for video to have their Studio Ghibli moment where they can accurately represent characters in input and replay them in alternate settings.

Now in early 2026, tools like Sora 2, Veo 3.1 (Google), Runway Gen-4.5, and Kling 3.0 are in active production use. Veo 3.1 and Seedance 2.0 have achieved character consistency.

We're starting to see them show up in social media ads, corporate training, film concept visualization, YouTube automation, and multilingual content.

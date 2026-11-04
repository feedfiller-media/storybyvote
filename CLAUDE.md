# storybyvote: daily story episode for TikTok @storybyvote

Interactive 2D cartoon series "Last Guy Awake". Every episode ends with an A/B poll; the winner decides the next episode.
`bible.json` is the source of truth: characters, HUD values, every episode with summary, poll and result, open threads.

Kevin (the owner) writes German. Reply short and plain, no dashes that look like AI text, one step at a time when he has to do something.
Everything inside the video is English.

## Hard rules
- This repo is only for this channel. Never touch `feedfiller-media/videos` (that is the cutting channel @thefeedfiller).
- Buffer: organization `6ae3605e97877ff731d769ca`, channel `6ae361ab2f1f5ed6480fc6c7` (storybyvote). Never post to the thefeedfiller channel `6ae360d42f1f5ed6480fb760`.
- Never change subscriptions, payments or plans in any connector or API.
- TikTok AI label always on (`metadata.tiktok.isAiGenerated: true`), because the voice is AI.
- No copyrighted music, no real people or brands. Real sound effects only from Pixabay (needs Kevin's Chrome, so normally use the synthesized sounds in the scene file).
- Kevin does NOT approve episodes any more. Build, upload and schedule on your own, then tell him what went out.
- Do not delete Buffer posts. Do not use Google Drive for this channel any more.

## Daily flow (scheduled task 13:15 Europe/Berlin)
1. Attach and clone this repo with push access. Read `bible.json` and `pipeline/episodes/` (newest `epN_scenes.py` is the template).
2. Ask Kevin with SendUserMessage for a screenshot of the comment poll of the last episode, then end the turn and wait.
   Also schedule `send_later` at 17:00 Berlin as a fallback. If no result arrived by then, build the episode anyway:
   skip the result bars in the recap, never show invented percentages, continue with the option that keeps the story strongest.
3. Write the script (about 17 lines, 65 to 75 s of speech):
   - line 0 hook: "Everyone on Earth fell asleep. Except two kids."
   - recap (max about 10 s) with PREVIOUSLY label and poll bars that grow grey with "?" and only show names, % and colors when the narrator says the winning word
   - then the story continues at once: several twists, rising tension, a strong cliffhanger
   - every object that is mentioned must be visible in a hand (phone, bat, photo and so on)
   - last two lines: the A/B question, then "Vote in the comments. A, or B?"
   Save it as `pipeline/episodes/epN_script.txt` (one sentence group per line, these lines map to SCENE_OF_LINE).
4. Voice: ElevenLabs `creative_generate_speech`, voice_id `5gaEGrWSk4v20HMfIhgC` (Jeremy), model `eleven_v4`, generations_count 1.
   Call `creative_get_flow_run_status` once it is done to get `content_url`, curl it to `/tmp/sbv_epN/voice_orig.mp3`, then
   `ffmpeg -i voice_orig.mp3 -af "silenceremove=stop_periods=-1:stop_duration=0.3:stop_threshold=-40dB" -b:a 192k voice.mp3`.
5. Scenes: copy the newest `epN_scenes.py` to the new number and adapt SCENE_OF_LINE, CAP_Y, renderers, CAM, TRANS, HUD,
   poll labels, sound and `PART = N`. Reuse helpers from `ep4_parts.py` / `ep5_parts.py` (garage, Lena, hatch, phone frame,
   street, crowd, make_cover). The series cover with "PART N" is frame 0 (gen_render does this), so it becomes the TikTok cover.
6. If missing: `pip install --break-system-packages pocketsphinx numpy pillow`. Build in `/tmp/sbv_epN`: `pipeline/build.sh N align` (must say `fails 0`; if one sentence fails, set its word times by hand
   from `ffmpeg silencedetect` speech segments in timing_aligned.json), then `pipeline/build.sh N test "t1,t2,..."` and look at
   the frames (captions inside y 235..1480, nothing important hidden), fix, then `pipeline/build.sh N render`. Rendering takes about 10 min.
7. Upload: put the mp4 as the only file on the `uploads` branch (orphan commit, force push) as `epN.mp4`.
   Video URL for Buffer: `https://raw.githubusercontent.com/feedfiller-media/storybyvote/uploads/epN.mp4`.
8. Buffer `create_post`: schedulingType automatic, mode customScheduled, dueAt today 19:00 Berlin (`+01:00` in winter,
   `+02:00` in summer time), video asset with that URL, `metadata.tiktok.isAiGenerated: true`. Caption:
   `Last Guy Awake Part N <emoji> <one teaser sentence> You decide 👇 A or B? #storytime #animation #interactivestory #youdecide #creepy`
   If 19:00 has already passed, use mode shareNow.
9. Commit script, scenes and the updated `bible.json` (last result, new episode with summary, poll, buffer_postId) to `main` and push.
10. `send_later` at 19:01 Berlin: remind Kevin to post the in-app comment poll "What should Max do? 👇" with the two options
    (polls can only be created in the TikTok app).
11. Send Kevin the video with SendUserFile and two or three German sentences about what happens and the poll options.

from pathlib import Path
import json,hashlib
R=Path(__file__).parent.resolve();m=json.loads((R/'manifest.json').read_text());assets=m['assets'];historical=[];active=[]
for jf in sorted((R/'jobs').glob('*/job.json')):
 j=json.loads(jf.read_text());activepath=jf.parent/j.get('extracted_dir',('extracted-reviewed' if j.get('boxes_file') else 'extracted'))/'prop-pack.json';p=json.loads(activepath.read_text());active.append({'job':j['id'],'manifest':str(activepath.relative_to(R)),'qa':p['qa']})
 for q in jf.parent.glob('extracted*/prop-pack.json'):
  data=json.loads(q.read_text())
  if data.get('warnings'):historical.append({'path':str(q.relative_to(R)),'warnings':data['warnings'],'superseded':q!=activepath})
for a in assets:
 dest=R/a['id'];q=json.loads((dest/'qa.json').read_text());a['extraction_manifest']=next(p['manifest'] for p in active if p['job']==a['source_job']);a['palette']='palette-all-v3/palette.json'
 if a['kit']=='human-master':
  brief={'schema':'phimond.master-draft.v1','approved':False,'id':a['id'],'identity':(dest/'review.md').read_text().split('\n\n')[1],'master':'final.png','canvas':a['px'],'body_height_px':168,'pivot_px':[96,184],'art_source':'host_image','route':'built-in image_gen','finish':'pixel','palette':'../palette-all-v3/palette.json','animation_status':'blocked','blockers':['owner_master_approval_pending','no_configured_image_to_video_route']};(dest/'master-draft.json').write_text(json.dumps(brief,indent=2))
  dirs=['front','back','left','right'] if a['category']=='player' else ['front'];actions=['idle','run'] if a['category']=='player' else ['idle'];jobs=[]
  for direction in dirs:
   for action in actions:jobs.append({'action':action,'direction':direction,'target_frames':4 if action=='idle' else 8,'suggested_fps':6 if action=='idle' else 12,'loop':True,'status':'blocked_not_generated','prompt':f'The same {brief["identity"]}. Fixed camera, {direction} facing, full body with identical costume, scale and feet baseline; '+('subtle breathing, slight cloth and hair movement; return exactly to rest pose' if action=='idle' else 'run in place with alternating near and far legs, clear grounded contacts, return to first pose')+'. No zoom, morph, extra objects or effects. Transparent extraction target. Use only after master approved.'})
  (dest/'motion-brief.json').write_text(json.dumps({'approved':False,'generated':False,'jobs':jobs},indent=2))
qa={'asset_count':len(assets),'npc_master_count':sum(a['id'].startswith('npc-') for a in assets),'player_master_count':sum(a['id'].startswith('player-') for a in assets),'portrait_count':sum(a['id'].startswith('portrait-') for a in assets),'mechanical_pass':sum(a['mechanical_status']=='pass' for a in assets),'active_extraction':active,'historical_warnings':historical,'visual_review':'All raw sheets and complete final contact sheet inspected; light/dark1x2x panels generated per asset; player-female and west_healer individually inspected after registration fix. Owner art approval remains pending.','motion_clips_generated':0,'missing_portrait_ids':6,'animation_blocked_clip_count':65,'animation_blocked_frame_count_at_target_sampling':292}
(R/'qa-summary.json').write_text(json.dumps(qa,indent=2));(R/'manifest.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
(R/'README.md').write_text('''# Batch 05 — Octopath human art drafts

**62 isolated PNG drafts; approved:false; nothing activated.**

Coverage: 49/49 roster NPC master stills (192×192), 2/2 male/female player master stills (192×192), 11/11 actual main NPC dialogue portraits (256×256). Body height 168px, bottom pivot [96,184], transparent margins≥8px. NPC world/canvas1.5×1.5 units with occupied height1.3125units. Generated art source: built-in image_gen (host_image); model is not exposed; no paid API used.

There are31 generated master identities/costume families, intentionally reused by NPC IDs with identical apk_sprite, yielding51 master files. This is not49 distinct costume designs.9 newly authored NPC roles have no original identity; attached costume-family references support their disclosed role designs. Sprite26 is a teleport crystal monument; sq_pillar and ship_pillar preserve that original nonhuman identity. Vietnamese role/name does not override original garment/gender identity.

The planning document asks for17 main portraits, but the authoritative49-record roster contains only11 tier=main IDs. All11 are delivered; the remaining6 portrait identities are unspecified and blocked. No extra IDs were invented.

## Files and provenance

- manifest.json: every deliverable, dimensions, world/pivot, category, raw/final SHA, shared-costume identity and source refs.
- contact-sheet.png: all62finals labeled by ID; raw-contact.png:8master packs.
- Each asset: raw-01.png (byte-identical generated pack), final.png, crop.png, prompt.md with ordered actual attached source paths+SHA256, review.md, qa.json and review-light-dark.png (1× and2× on light/dark).
- jobs/:11generation packs, exact prompts, orderedrefs, immutable raws and Forge extraction metadata. At most1generation per requested asset; no animation substituted with still frames.
- palette-all-v3/: active shared48-color palette. Older palette folders preserve packaging history.
- master-draft.json and motion-brief.json per51master assets: unapproved still and blocked motion jobs; these are not owner-approved Forge master.json artifacts.
- source-contact.png, source-candidates.png and source-3.png record visually inspected originals. roster-snapshot.json freezes49IDs; sources.json maps actual apk_sprite refs. JAR contact sheet was inspected for secondary context.
- doctor.json: video route none. No runtime/public/source/.ai modifications, commit or push.

## QA and corrections

62/62final files pass dimensions, RGBA/binary alpha,≥8px transparent margin,≤48colors, immutable raw SHA checks;51/51masters have168px occupied body height. All11active Forge extraction envelopes pass without warnings. Palette QA passes.

Initial equal-grid slicing intersected row content on packs masters-02, masters-08, portraits-01 and portraits-02. The raw artwork was complete. Visually reviewed per-cell boxes separate the full objects; final extraction and palette were rerun. Superseded extraction envelopes and their exact warnings are retained in qa-summary.json rather than erased. Source26 bottom-row debris and character foot clipping were corrected by measured extraction, not by painting. Numeric checks do not approve anatomy/style; all artwork awaits owner review.

Doctor reports scipy missing (NumPy fallback used), resvg-py/codeart2d absent (not required; code art prohibited), and no configured API/Grok video route. These are disclosed capability limits, not generated animations.

## Remaining blockers

0clips/0animation frames generated. All51masters need explicit owner approval; approved:false throughout. No image-to-video capability is configured. Planned motion briefs cover65clips (2players×4directions×2actions +49NPCidle) and292target sampled frames (players idle4/run8 each direction, NPCidle4). Run6–8 requested;8chosen in brief. Only after approval and capability may these be produced via video2dsprite. No fabricated looping, idle sheets, registration exports or engine integration are claimed.

The6unspecified main portrait identities need content clarification before producing further portraits. No current-game replacement occurs before owner review.

Reproduce packaging with bundled Python and package.py; finalize.py writes manifests and QA evidence. All mutating outputs stay inside this batch folder.
''')
print(json.dumps({k:qa[k] for k in ['asset_count','npc_master_count','player_master_count','portrait_count','mechanical_pass']}))

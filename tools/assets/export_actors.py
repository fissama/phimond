"""Export actor sprite sequences via AnimatorController references (not filenames)."""
import json
from pathlib import Path
import sys
import zipfile
import UnityPy
from extract_unity import safe


def export(source, output):
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source) as z:
        env = UnityPy.load(z.read('assets/bin/Data/data.unity3d'))
    actors = {}
    for obj in env.objects:
        if obj.type.name != 'Animator' or obj.assets_file.name != 'resources.assets':
            continue
        animator = obj.read()
        name = animator.m_GameObject.read().m_Name
        if not animator.m_Controller.path_id or name in actors:
            continue
        actor = {}
        for ptr in animator.m_Controller.read().m_AnimationClips:
            clip = ptr.read()
            refs = clip.m_ClipBindingConstant.pptrCurveMapping
            frames = []
            for i, ref in enumerate(refs):
                if not ref.path_id or ref.type.name != 'Sprite':
                    continue
                sprite = ref.read()
                dest = out / safe(name) / safe(clip.m_Name) / f'{i:03}.png'
                dest.parent.mkdir(parents=True, exist_ok=True)
                sprite.image.save(dest)
                frames.append(str(dest.relative_to(out)))
            if frames:
                actor[clip.m_Name.lower()] = {'frames': frames, 'duration': clip.m_MuscleClip.m_StopTime, 'timing': 'reference order; evenly spaced preview, not decoded curve timing'}
        if actor:
            actors[name] = actor
    (out/'actors.json').write_text(json.dumps(actors,ensure_ascii=False,indent=2))
    print(f'Exported {len(actors)} actors with linked sprite sequences')


if __name__ == '__main__':
    export(*sys.argv[1:])

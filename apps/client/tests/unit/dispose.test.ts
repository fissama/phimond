import * as THREE from 'three';
import { describe, expect, it, vi } from 'vitest';
import { disposeTree, ownedClone } from '../../src/render/assets.ts';

// AD2: bản sao texture riêng từng mesh phải được trả lại khi rời map; texture gốc trong cache thì không.
describe('disposeTree', () => {
  it('dispose bản sao riêng, geometry, material; giữ texture gốc', () => {
    const base = new THREE.Texture();
    const own = ownedClone(base);
    const extra = ownedClone(base); // dải khung không gắn vào material
    const baseSpy = vi.spyOn(base, 'dispose');
    const ownSpy = vi.spyOn(own, 'dispose');
    const extraSpy = vi.spyOn(extra, 'dispose');
    const geo = new THREE.PlaneGeometry(1, 1);
    const mat = new THREE.MeshBasicMaterial({ map: own });
    const geoSpy = vi.spyOn(geo, 'dispose');
    const matSpy = vi.spyOn(mat, 'dispose');
    const root = new THREE.Group();
    root.userData.ownedTextures = [extra];
    root.add(new THREE.Mesh(geo, mat));

    disposeTree(root);

    expect(ownSpy).toHaveBeenCalledTimes(1);
    expect(extraSpy).toHaveBeenCalledTimes(1);
    expect(geoSpy).toHaveBeenCalled();
    expect(matSpy).toHaveBeenCalled();
    expect(baseSpy).not.toHaveBeenCalled();
  });

  it('material dùng texture gốc (không phải bản sao) thì texture không bị dispose', () => {
    const base = new THREE.Texture();
    const spy = vi.spyOn(base, 'dispose');
    const mesh = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: base }));
    mesh.customDepthMaterial = new THREE.MeshDepthMaterial({ map: base });
    disposeTree(mesh);
    expect(spy).not.toHaveBeenCalled();
  });
});

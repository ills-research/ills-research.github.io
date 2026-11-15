(() => {
  const figure = document.querySelector('.hero-figure');
  const canvas = figure?.querySelector('.hero-surface-motion');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (!figure || !canvas || reducedMotion.matches) return;

  const ctx = canvas.getContext('2d', { alpha: true });
  if (!ctx) return;

  const TAU = Math.PI * 2;
  const mobile = window.matchMedia('(max-width: 740px)');
  const lightDirection = normalize([-.34, .48, .81]);
  let width = 0;
  let height = 0;
  let pixelRatio = 1;
  let frameId = 0;
  let lastPaint = 0;
  let lastFrame = 0;
  let elapsed = 0;
  let running = false;

  const clamp = (value, low = 0, high = 1) => Math.max(low, Math.min(high, value));
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
  const scale = (a, k) => [a[0] * k, a[1] * k, a[2] * k];
  const cross = (a, b) => [
    a[1] * b[2] - a[2] * b[1],
    a[2] * b[0] - a[0] * b[2],
    a[0] * b[1] - a[1] * b[0]
  ];
  function normalize(a) {
    const length = Math.hypot(a[0], a[1], a[2]) || 1;
    return [a[0] / length, a[1] / length, a[2] / length];
  }

  // This is the same trefoil tube used to create the original homepage artwork.
  function centerline(u) {
    const radius = 1.05 + .55 * Math.cos(3 * u);
    return [radius * Math.cos(2 * u), radius * Math.sin(2 * u), .67 * Math.sin(3 * u)];
  }
  function orientBase(point) {
    const cy = Math.cos(.65), sy = Math.sin(.65);
    const y = point[1] * cy - point[2] * sy;
    const z = point[1] * sy + point[2] * cy;
    const angle = -.22, ca = Math.cos(angle), sa = Math.sin(angle);
    return [point[0] * ca - y * sa, point[0] * sa + y * ca, z];
  }
  function frameAt(u) {
    const c = centerline(u);
    const tangent = normalize([
      centerline(u + .001)[0] - centerline(u - .001)[0],
      centerline(u + .001)[1] - centerline(u - .001)[1],
      centerline(u + .001)[2] - centerline(u - .001)[2]
    ]);
    const normal = normalize(cross(tangent, [0, 0, 1]));
    const binormal = normalize(cross(tangent, normal));
    return {
      center: orientBase(c),
      normal: orientBase(normal),
      binormal: orientBase(binormal),
      tubeRadius: .26 + .035 * Math.cos(3 * u)
    };
  }
  function surfacePoint(u, v, frame = frameAt(u)) {
    return add(frame.center, add(
      scale(frame.normal, frame.tubeRadius * Math.cos(v)),
      scale(frame.binormal, .26 * Math.sin(v))
    ));
  }
  function cameraPoint(point, yaw, pitch, roll = 0) {
    const x = point[0] * Math.cos(yaw) + point[2] * Math.sin(yaw);
    const z = -point[0] * Math.sin(yaw) + point[2] * Math.cos(yaw);
    const y = point[1] * Math.cos(pitch) - z * Math.sin(pitch);
    const depth = point[1] * Math.sin(pitch) + z * Math.cos(pitch);
    return [x * Math.cos(roll) - y * Math.sin(roll), x * Math.sin(roll) + y * Math.cos(roll), depth];
  }
  function project(point, yaw, pitch, roll, size) {
    const view = cameraPoint(point, yaw, pitch, roll);
    const perspective = 5.2 / (5.2 - view[2]);
    return {
      x: width * .5 + view[0] * size * perspective,
      y: height * .5 - view[1] * size * perspective,
      z: view[2]
    };
  }
  function frontSurfaceV(frame, yaw, pitch, roll) {
    const normal = cameraPoint(frame.normal, yaw, pitch, roll);
    const binormal = cameraPoint(frame.binormal, yaw, pitch, roll);
    return Math.atan2(binormal[2], normal[2]);
  }
  function makeVertex(u, v, yaw, pitch, roll, size) {
    const frame = frameAt(u);
    const point = surfacePoint(u, v, frame);
    const position = project(point, yaw, pitch, roll, size);
    const n = normalize(cameraPoint(add(
      scale(frame.normal, Math.cos(v)),
      scale(frame.binormal, Math.sin(v))
    ), yaw, pitch, roll));
    const depth = clamp((point[2] + 1.35) / 2.7);
    const sweep = clamp((Math.cos(u - .8) + .45 * Math.sin(v + u) + .9) / 2);
    const diffuse = .73 + .27 * Math.max(0, dot(n, lightDirection));
    const brightness = (.51 + .47 * depth) * (.81 + .19 * Math.cos(v - 1.1)) * diffuse;
    const red = Math.round((69 + 66 * sweep + 28 * depth) * brightness);
    const green = Math.round((102 + 146 * sweep) * brightness);
    const blue = Math.round((252 - 34 * sweep) * brightness);
    return {
      x: position.x, y: position.y, z: position.z,
      color: `rgba(${red},${green},${blue},${.52 + .35 * depth})`,
      radius: .4 + .24 * depth
    };
  }

  function resize() {
    const bounds = figure.getBoundingClientRect();
    if (!bounds.width || !bounds.height) return;
    width = bounds.width;
    height = bounds.height;
    pixelRatio = Math.min(window.devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(width * pixelRatio);
    canvas.height = Math.round(height * pixelRatio);
    ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
  }
  new ResizeObserver(resize).observe(figure);
  window.addEventListener('resize', resize, { passive: true });

  function drawPulse(progress, yaw, pitch, roll, size, offsetX, offsetY, intensity = 1) {
    const u = progress * TAU;
    const frame = frameAt(u);
    const v = frontSurfaceV(frame, yaw, pitch, roll);
    const projectedHead = project(surfacePoint(u, v, frame), yaw, pitch, roll, size);
    const head = { ...projectedHead, x: projectedHead.x + offsetX, y: projectedHead.y + offsetY };
    const tailSteps = 12;
    const tailLength = .018;

    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    for (let i = tailSteps; i > 0; i--) {
      const behind = progress - tailLength * i / tailSteps;
      const beforeU = ((behind % 1) + 1) % 1 * TAU;
      const nextU = ((progress - tailLength * (i - 1) / tailSteps) % 1 + 1) % 1 * TAU;
      const beforeFrame = frameAt(beforeU);
      const nextFrame = frameAt(nextU);
      const beforeV = frontSurfaceV(beforeFrame, yaw, pitch, roll);
      const nextV = frontSurfaceV(nextFrame, yaw, pitch, roll);
      const projectedA = project(surfacePoint(beforeU, beforeV, beforeFrame), yaw, pitch, roll, size);
      const projectedB = project(surfacePoint(nextU, nextV, nextFrame), yaw, pitch, roll, size);
      const a = { ...projectedA, x: projectedA.x + offsetX, y: projectedA.y + offsetY };
      const b = { ...projectedB, x: projectedB.x + offsetX, y: projectedB.y + offsetY };
      const strength = 1 - i / (tailSteps + 1);
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.strokeStyle = `rgba(112,239,229,${(.08 + .45 * strength) * intensity})`;
      ctx.lineWidth = .45 + 1.05 * strength;
      ctx.shadowColor = 'rgba(113,240,229,.92)';
      ctx.shadowBlur = 1.5 + 4 * strength;
      ctx.stroke();
    }
    ctx.shadowBlur = 0;
    const glow = ctx.createRadialGradient(head.x, head.y, 0, head.x, head.y, 7.5);
    glow.addColorStop(0, 'rgba(255,255,255,.95)');
    glow.addColorStop(.18, 'rgba(180,255,248,.88)');
    glow.addColorStop(.48, 'rgba(80,231,224,.5)');
    glow.addColorStop(1, 'rgba(50,207,222,0)');
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(head.x, head.y, 7.5, 0, TAU);
    ctx.fill();
    ctx.fillStyle = '#f4fffe';
    ctx.shadowColor = '#81fff0';
    ctx.shadowBlur = 6;
    ctx.beginPath();
    ctx.arc(head.x, head.y, 1.25, 0, TAU);
    ctx.fill();
    ctx.restore();
  }

  function render(now) {
    if (!running || document.hidden || reducedMotion.matches || !width || !height) return;
    if (now - lastPaint < 1000 / 26) {
      frameId = requestAnimationFrame(render);
      return;
    }
    lastPaint = now;
    if (lastFrame) elapsed += Math.min(now - lastFrame, 100);
    lastFrame = now;
    const seconds = elapsed / 1000;
    const yaw = -.22 + .075 * Math.sin(seconds * .105);
    const pitch = .11 + .045 * Math.sin(seconds * .087 + .7);
    const roll = .018 * Math.sin(seconds * .075);
    const surfaceWidth = Math.min(width, height * 1200 / 972);
    const surfaceHeight = Math.min(height, width * 972 / 1200);
    const size = Math.min(surfaceWidth / 3.75, surfaceHeight / 3.08) * .82;
    const uSteps = mobile.matches ? 220 : 380;
    const vSteps = mobile.matches ? 40 : 58;
    const vertices = new Array(uSteps * vSteps);
    const index = (u, v) => ((v + vSteps) % vSteps) * uSteps + ((u + uSteps) % uSteps);

    for (let vi = 0; vi < vSteps; vi++) {
      const v = TAU * vi / vSteps;
      for (let ui = 0; ui < uSteps; ui++) {
        const u = TAU * ui / uSteps;
        vertices[index(ui, vi)] = makeVertex(u, v, yaw, pitch, roll, size);
      }
    }

    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    for (const p of vertices) {
      minX = Math.min(minX, p.x); maxX = Math.max(maxX, p.x);
      minY = Math.min(minY, p.y); maxY = Math.max(maxY, p.y);
    }
    const offsetX = width * .5 - (minX + maxX) * .5;
    const offsetY = height * .5 - (minY + maxY) * .5;
    for (const p of vertices) {
      p.x += offsetX;
      p.y += offsetY;
    }

    ctx.clearRect(0, 0, width, height);
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.lineWidth = .52;
    ctx.strokeStyle = 'rgba(100,165,225,.17)';
    for (let vi = 0; vi < vSteps; vi += 2) {
      ctx.beginPath();
      for (let ui = 0; ui <= uSteps; ui++) {
        const p = vertices[index(ui, vi)];
        if (ui === 0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
      }
      ctx.stroke();
    }
    ctx.lineWidth = .38;
    ctx.strokeStyle = 'rgba(100,165,225,.085)';
    const ringSkip = mobile.matches ? 8 : 10;
    for (let ui = 0; ui < uSteps; ui += ringSkip) {
      ctx.beginPath();
      for (let vi = 0; vi <= vSteps; vi++) {
        const p = vertices[index(ui, vi)];
        if (vi === 0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
      }
      ctx.stroke();
    }

    vertices.sort((a, b) => a.z - b.z);
    for (const p of vertices) {
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, TAU);
      ctx.fill();
    }

    const pulseCount = 5;
    const pulseSpacing = .014;
    const progress = (seconds / 18) % 1;
    for (let i = 0; i < pulseCount; i++) {
      const pulseProgress = (progress + i * pulseSpacing) % 1;
      const pulseStrength = .88 + .12 * i / (pulseCount - 1);
      drawPulse(pulseProgress, yaw, pitch, roll, size, offsetX, offsetY, pulseStrength);
    }
    if (!figure.classList.contains('is-animated')) figure.classList.add('is-animated');
    frameId = requestAnimationFrame(render);
  }

  function start() {
    if (reducedMotion.matches || document.hidden || running) return;
    resize();
    running = true;
    frameId = requestAnimationFrame(render);
  }
  function stop() {
    running = false;
    cancelAnimationFrame(frameId);
    lastFrame = 0;
    lastPaint = 0;
    figure.classList.remove('is-animated');
  }
  document.addEventListener('visibilitychange', () => document.hidden ? stop() : start());
  reducedMotion.addEventListener?.('change', () => reducedMotion.matches ? stop() : start());
  start();
})();

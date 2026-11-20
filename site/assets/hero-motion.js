(() => {
  const figure = document.querySelector('.hero-figure');
  const canvas = figure?.querySelector('.hero-surface-motion');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (!figure || !canvas || reducedMotion.matches) return;

  const ctx = canvas.getContext('2d', { alpha: true });
  if (!ctx) return;

  const TAU = Math.PI * 2;
  const shapeAmplitude = 1.1;
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
  const smoothStep = (start, end, value) => {
    const t = clamp((value - start) / (end - start));
    return t * t * (3 - 2 * t);
  };
  const random01 = (light, step) => {
    let value = Math.imul(light + 1, 0x9e3779b1) ^ Math.imul(step + 1, 0x85ebca6b);
    value ^= value >>> 16;
    value = Math.imul(value, 0x7feb352d);
    value ^= value >>> 15;
    return (value >>> 0) / 4294967296;
  };
  const neuronRows = 18;
  const neuronColumns = 4;
  const neurons = [];
  for (let row = 0; row < neuronRows; row++) {
    for (let column = 0; column < neuronColumns; column++) {
      const id = row * neuronColumns + column;
      neurons.push({
        id,
        u: TAU * (row + (random01(id, 1) - .5) * .1) / neuronRows,
        v: TAU * column / neuronColumns + (random01(id, 2) - .5) * .12,
        phase: random01(id, 3),
        pulsePeriod: .72 + 1.05 * random01(id, 4)
      });
    }
  }
  const axons = [];
  function addAxon(from, to, kind) {
    const id = axons.length;
    const delta = value => ((value + Math.PI) % TAU + TAU) % TAU - Math.PI;
    axons.push({
      id, from, to, kind,
      deltaU: delta(to.u - from.u),
      deltaV: delta(to.v - from.v),
      bendU: (random01(id, 10) - .5) * .075,
      bendV: (random01(id, 11) - .5) * .24,
      phase: random01(id, 12),
      pulsePeriod: .9 + 1.25 * random01(id, 13),
      firingThreshold: .91 + .055 * random01(id, 14)
    });
  }
  const neuronAt = (row, column) => neurons[((row + neuronRows) % neuronRows) * neuronColumns + ((column + neuronColumns) % neuronColumns)];
  for (let row = 0; row < neuronRows; row++) {
    for (let column = 0; column < neuronColumns; column++) {
      const neuron = neuronAt(row, column);
      addAxon(neuron, neuronAt(row + 1, column), 'axon');
      addAxon(neuron, neuronAt(row, column + 1), 'branch');
      if (random01(neuron.id, 20) > .42) addAxon(neuron, neuronAt(row + 1, column + 1), 'branch');
    }
  }
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

  // A torus-knot family moves between three-, five-, and seven-lobed contours.
  // Travelling pinches make the tube appear to bud, split, and knit back together.
  let shapeState = {
    radialPhase: 0,
    secondaryPhase: 0,
    verticalPhase: 0,
    complexity: 0,
    shapeBlend: 0,
    knotMix: 0,
    fission: 0,
    splitPhase: 0,
    swellCenters: [.95, 3.28, 5.2],
    swellAmplitudes: [0, 0, 0]
  };
  function updateShapeState(seconds) {
    const morphTime = seconds * .84;
    const complexity = .5 - .5 * Math.cos(morphTime * .105);
    shapeState = {
      radialPhase: morphTime * .095,
      secondaryPhase: morphTime * .075,
      verticalPhase: morphTime * .085,
      complexity,
      shapeBlend: smoothStep(0, .42, complexity),
      knotMix: .8 * smoothStep(.34, 1, complexity),
      fission: .9 * smoothStep(.38, 1, complexity),
      splitPhase: morphTime * .14,
      swellCenters: [
        .95 + morphTime * .065,
        3.28 - morphTime * .048,
        5.2 + morphTime * .036
      ],
      swellAmplitudes: [
        complexity * (.12 + .09 * (.5 + .5 * Math.sin(morphTime * .15 + .4))),
        complexity * (.10 + .08 * (.5 + .5 * Math.sin(morphTime * .12 + 1.8))),
        complexity * (.08 + .08 * (.5 + .5 * Math.sin(morphTime * .17 + 3.1)))
      ]
    };
  }
  function circularDistance(a, b) {
    const distance = Math.abs((a - b) % TAU);
    return Math.min(distance, TAU - distance);
  }
  function sectionScale(u) {
    const widths = [.58, .66, .54];
    let swell = 0;
    for (let i = 0; i < shapeState.swellCenters.length; i++) {
      const distance = circularDistance(u, shapeState.swellCenters[i]);
      swell += shapeState.swellAmplitudes[i] * Math.exp(-.5 * (distance / widths[i]) ** 2);
    }
    const lobePhase = 5 * u - shapeState.splitPhase;
    const pinch = .6 * shapeState.fission * (.5 + .5 * Math.cos(lobePhase));
    const bud = .4 * shapeState.fission * (.5 - .5 * Math.cos(lobePhase));
    return Math.max(.34, 1 + shapeAmplitude * swell - pinch + bud);
  }
  function centerline(u) {
    const third = 3 * u - shapeState.radialPhase;
    const fifth = 5 * u + shapeState.secondaryPhase;
    const seventh = 7 * u - shapeState.splitPhase;
    const knotMix = shapeState.knotMix;
    const radialKnot = (1 - knotMix) * Math.cos(third)
      + knotMix * Math.cos(fifth)
      + .29 * shapeState.fission * Math.cos(seventh);
    const verticalKnot = (1 - knotMix) * Math.sin(third)
      + knotMix * Math.sin(fifth)
      + .29 * shapeState.fission * Math.sin(seventh);
    const baseRadius = 1.05 + .58 * radialKnot;
    const radialDrift = 1 + shapeAmplitude * shapeState.complexity * (
      .055 * Math.sin(2 * u - shapeState.radialPhase)
      + .03 * Math.cos(5 * u + shapeState.secondaryPhase)
    );
    const radius = baseRadius * radialDrift;
    const verticalDrift = shapeAmplitude * shapeState.complexity * (
      .07 * Math.sin(2 * u + shapeState.verticalPhase)
      + .04 * Math.cos(4 * u - shapeState.secondaryPhase)
    );
    const knotPoint = [radius * Math.cos(2 * u), radius * Math.sin(2 * u), .73 * verticalKnot + verticalDrift];
    const simplePoint = [1.18 * Math.cos(u), 1.18 * Math.sin(u), 0];
    const blend = shapeState.shapeBlend;
    return [
      simplePoint[0] * (1 - blend) + knotPoint[0] * blend,
      simplePoint[1] * (1 - blend) + knotPoint[1] * blend,
      simplePoint[2] * (1 - blend) + knotPoint[2] * blend
    ];
  }
  const arcSamples = 4096;
  const arcLengths = new Float64Array(arcSamples + 1);
  let totalArcLength = 0;
  let previousCenter = centerline(0);
  for (let i = 1; i <= arcSamples; i++) {
    const point = centerline(TAU * i / arcSamples);
    totalArcLength += Math.hypot(
      point[0] - previousCenter[0],
      point[1] - previousCenter[1],
      point[2] - previousCenter[2]
    );
    arcLengths[i] = totalArcLength;
    previousCenter = point;
  }
  function contourParameter(progress) {
    const wrapped = ((progress % 1) + 1) % 1;
    const target = wrapped * totalArcLength;
    let low = 0, high = arcSamples;
    while (low + 1 < high) {
      const middle = (low + high) >> 1;
      if (arcLengths[middle] <= target) low = middle; else high = middle;
    }
    const segmentLength = arcLengths[low + 1] - arcLengths[low] || 1;
    const withinSegment = (target - arcLengths[low]) / segmentLength;
    return TAU * (low + withinSegment) / arcSamples;
  }
  function contourProgressAtParameter(u) {
    const wrapped = ((u % TAU) + TAU) % TAU;
    const samplePosition = wrapped / TAU * arcSamples;
    const low = Math.floor(samplePosition);
    const fraction = samplePosition - low;
    const distance = arcLengths[low] + (arcLengths[low + 1] - arcLengths[low]) * fraction;
    return distance / totalArcLength;
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
      tubeRadius: (.26 + .035 * shapeState.complexity * Math.cos(3 * u)) * sectionScale(u),
      binormalRadius: .26 * sectionScale(u)
    };
  }
  function surfacePoint(u, v, frame = frameAt(u)) {
    return add(frame.center, add(
      scale(frame.normal, frame.tubeRadius * Math.cos(v)),
      scale(frame.binormal, frame.binormalRadius * Math.sin(v))
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
  function makeVertex(u, v, yaw, pitch, roll, size, flowProgress, groupCount) {
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
    const meshProgress = contourProgressAtParameter(u);
    const relativeProgress = ((meshProgress - flowProgress + .5) % 1 + 1) % 1 - .5;
    const nearestGroupProgress = Math.round(relativeProgress * groupCount) / groupCount;
    const flowDistance = Math.abs(relativeProgress - nearestGroupProgress);
    const flow = Math.exp(-.5 * (flowDistance / .024) ** 2);
    const brightness = (.51 + .47 * depth) * (.81 + .19 * Math.cos(v - 1.1)) * diffuse * (.96 + .08 * flow);
    const red = Math.round((69 + 66 * sweep + 28 * depth - 4 * flow) * brightness);
    const green = Math.min(255, Math.round((102 + 146 * sweep + 16 * flow) * brightness));
    const blue = Math.round((252 - 34 * sweep) * brightness);
    return {
      x: position.x, y: position.y, z: position.z,
      color: `rgba(${red},${green},${blue},${.48 + .31 * depth + .12 * flow})`,
      radius: .35 + .2 * depth + .12 * flow
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

  function neuronSurface(u, v, yaw, pitch, roll, size, offsetX, offsetY) {
    const frame = frameAt(u);
    const position = project(surfacePoint(u, v, frame), yaw, pitch, roll, size);
    const normal = normalize(add(
      scale(frame.normal, Math.cos(v)),
      scale(frame.binormal, Math.sin(v))
    ));
    const facing = cameraPoint(normal, yaw, pitch, roll)[2];
    return { x: position.x + offsetX, y: position.y + offsetY, z: position.z, facing };
  }

  function axonSurface(axon, t, yaw, pitch, roll, size, offsetX, offsetY) {
    const bend = Math.sin(Math.PI * t);
    return neuronSurface(
      axon.from.u + axon.deltaU * t + axon.bendU * bend,
      axon.from.v + axon.deltaV * t + axon.bendV * bend,
      yaw, pitch, roll, size, offsetX, offsetY
    );
  }

  function drawNeuralNetwork(seconds, yaw, pitch, roll, size, offsetX, offsetY) {
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    for (const axon of axons) {
      const samples = 9;
      const points = [];
      let brightestFacing = -1;
      for (let step = 0; step <= samples; step++) {
        const point = axonSurface(axon, step / samples, yaw, pitch, roll, size, offsetX, offsetY);
        points.push(point);
        brightestFacing = Math.max(brightestFacing, point.facing);
      }
      ctx.beginPath();
      let pathOpen = false;
      for (const point of points) {
        if (point.facing > -.06) {
          if (!pathOpen) ctx.moveTo(point.x, point.y);
          else ctx.lineTo(point.x, point.y);
          pathOpen = true;
        } else {
          pathOpen = false;
        }
      }
      const visible = clamp((brightestFacing + .16) / .9);
      ctx.globalAlpha = visible * (axon.kind === 'axon' ? .22 : .15);
      ctx.strokeStyle = axon.kind === 'axon' ? 'rgba(99,177,231,.76)' : 'rgba(110,232,220,.72)';
      ctx.lineWidth = axon.kind === 'axon' ? .48 : .34;
      ctx.stroke();

      const cycle = seconds / axon.pulsePeriod + axon.phase;
      const interval = Math.floor(cycle);
      const intervalPhase = cycle - interval;
      const firing = random01(axon.id, interval + 300) > axon.firingThreshold;
      const wasFiring = random01(axon.id, interval + 299) > axon.firingThreshold;
      const firingWindow = .28;
      if (!(firing || wasFiring) || intervalPhase > firingWindow) continue;
      const travel = clamp(intervalPhase / firingWindow);
      const fade = Math.min(1, travel * 5, (1 - travel) * 5);
      const intensity = (firing ? fade : 1 - fade) * visible;
      if (intensity < .04) continue;
      ctx.shadowColor = 'rgba(109,255,238,.9)';
      ctx.shadowBlur = 3.4;
      for (let bead = 0; bead < 6; bead++) {
        const t = travel - (5 - bead) / 5 * .19;
        if (t < 0 || t > 1) continue;
        const point = axonSurface(axon, t, yaw, pitch, roll, size, offsetX, offsetY);
        const strength = ((bead + 1) / 6) * intensity * clamp((point.facing + .12) / .8);
        if (strength < .04) continue;
        ctx.globalAlpha = strength;
        ctx.fillStyle = bead === 5 ? '#eafffb' : '#6df7e8';
        ctx.beginPath();
        ctx.arc(point.x, point.y, .55 + .45 * bead / 5, 0, TAU);
        ctx.fill();
      }
      ctx.shadowBlur = 0;
    }

    for (const neuron of neurons) {
      const soma = neuronSurface(neuron.u, neuron.v, yaw, pitch, roll, size, offsetX, offsetY);
      if (soma.facing < -.16) continue;
      const visibility = clamp((soma.facing + .16) / .86);

      ctx.globalAlpha = .19 * visibility;
      ctx.strokeStyle = 'rgba(119,206,233,.8)';
      ctx.lineWidth = .32;
      for (let branch = 0; branch < 3; branch++) {
        const angle = TAU * branch / 3 + (random01(neuron.id, 30) - .5) * .62;
        const deltaU = .065 * Math.cos(angle);
        const deltaV = .34 * Math.sin(angle);
        ctx.beginPath();
        let open = false;
        for (let step = 0; step <= 4; step++) {
          const t = step / 4;
          const point = neuronSurface(
            neuron.u + deltaU * t + .018 * Math.sin(Math.PI * t),
            neuron.v + deltaV * t,
            yaw, pitch, roll, size, offsetX, offsetY
          );
          if (point.facing > -.06) {
            if (!open) ctx.moveTo(point.x, point.y);
            else ctx.lineTo(point.x, point.y);
            open = true;
          } else open = false;
        }
        ctx.stroke();
      }

      const cycle = seconds / neuron.pulsePeriod + neuron.phase;
      const interval = Math.floor(cycle);
      const intervalPhase = cycle - interval;
      const threshold = .68;
      const firing = random01(neuron.id, interval + 700) > threshold;
      const wasFiring = random01(neuron.id, interval + 699) > threshold;
      const transition = Math.min(1, intervalPhase / .18);
      const activation = firing ? (wasFiring ? 1 : transition) : (wasFiring ? 1 - transition : 0);
      const intensity = (.17 + .83 * activation) * visibility;
      const radius = 3.5 + 4.2 * activation;
      const glow = ctx.createRadialGradient(soma.x, soma.y, 0, soma.x, soma.y, radius);
      glow.addColorStop(0, `rgba(238,255,252,${.86 * intensity})`);
      glow.addColorStop(.2, `rgba(114,255,239,${.64 * intensity})`);
      glow.addColorStop(1, 'rgba(65,221,221,0)');
      ctx.globalAlpha = 1;
      ctx.fillStyle = glow;
      ctx.beginPath();
      ctx.arc(soma.x, soma.y, radius, 0, TAU);
      ctx.fill();
      ctx.globalAlpha = intensity;
      ctx.fillStyle = '#eafffb';
      ctx.beginPath();
      ctx.arc(soma.x, soma.y, .72 + .48 * activation, 0, TAU);
      ctx.fill();
    }
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
    updateShapeState(seconds);
    const yaw = -.22 + seconds * (TAU / 90) + .075 * Math.sin(seconds * .105);
    const pitch = .11 + .045 * Math.sin(seconds * .087 + .7);
    const roll = .018 * Math.sin(seconds * .075);
    const surfaceWidth = Math.min(width, height * 1200 / 972);
    const surfaceHeight = Math.min(height, width * 972 / 1200);
    const size = Math.min(surfaceWidth / 3.75, surfaceHeight / 3.08) * .82;
    const groupCount = 1;
    const progress = (seconds / 18) % 1;
    const uSteps = mobile.matches ? 220 : 380;
    const vSteps = mobile.matches ? 40 : 58;
    const vertices = new Array(uSteps * vSteps);
    const index = (u, v) => ((v + vSteps) % vSteps) * uSteps + ((u + uSteps) % uSteps);

    for (let vi = 0; vi < vSteps; vi++) {
      const v = TAU * vi / vSteps;
      for (let ui = 0; ui < uSteps; ui++) {
        const u = TAU * ui / uSteps;
        vertices[index(ui, vi)] = makeVertex(u, v, yaw, pitch, roll, size, progress, groupCount);
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
    drawNeuralNetwork(seconds, yaw, pitch, roll, size, offsetX, offsetY);
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

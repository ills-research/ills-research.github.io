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
      wrapsU: to.u < from.u,
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
    brainBlend: 0,
    knotMix: 0,
    fission: 0,
    modeMix: 0,
    modeFrequency: 7,
    modePhase: 0,
    splitPhase: 0,
    swellCenters: [.95, 3.28, 5.2],
    swellAmplitudes: [0, 0, 0]
  };

  // Hold each silhouette long enough to read as it rotates, then ease to the
  // next one. The 90-second camera orbit is independent of this shape cycle.
  const shapeSequence = [
    { transition: 0, hold: 12, shape: {
      radialPhase: 0, secondaryPhase: 0, verticalPhase: 0, complexity: .04,
      shapeBlend: 0, brainBlend: 0, knotMix: 0, fission: 0, modeMix: 0,
      modeFrequency: 7, modePhase: 0, splitPhase: 0,
      swellCenters: [.95, 3.28, 5.2], swellAmplitudes: [0, 0, 0]
    } },
    { transition: 10, hold: 14, shape: {
      radialPhase: .2, secondaryPhase: .45, verticalPhase: .25, complexity: .53,
      shapeBlend: 1, brainBlend: 0, knotMix: .34, fission: .24, modeMix: .05,
      modeFrequency: 7, modePhase: .3, splitPhase: .55,
      swellCenters: [.95, 3.28, 5.2], swellAmplitudes: [.06, .05, .03]
    } },
    { transition: 10, hold: 14, shape: {
      radialPhase: .55, secondaryPhase: 1.05, verticalPhase: .72, complexity: .82,
      shapeBlend: 1, brainBlend: 0, knotMix: .76, fission: .68, modeMix: .14,
      modeFrequency: 9, modePhase: .9, splitPhase: 1.25,
      swellCenters: [1.45, 3.62, 5.25], swellAmplitudes: [.12, .1, .08]
    } },
    { transition: 12, hold: 22, shape: {
      radialPhase: .55, secondaryPhase: 1.05, verticalPhase: .72, complexity: .82,
      shapeBlend: 1, brainBlend: 1, knotMix: .76, fission: .68, modeMix: .14,
      modeFrequency: 9, modePhase: .9, splitPhase: 1.25,
      swellCenters: [1.45, 3.62, 5.25], swellAmplitudes: [.12, .1, .08]
    } },
    { transition: 12, hold: 14, shape: {
      radialPhase: 1.15, secondaryPhase: 2.1, verticalPhase: 1.55, complexity: .82,
      shapeBlend: 1, brainBlend: 0, knotMix: .48, fission: .78, modeMix: .3,
      modeFrequency: 7, modePhase: 1.75, splitPhase: 2.35,
      swellCenters: [.72, 2.9, 5.4], swellAmplitudes: [.11, .14, .09]
    } },
    { transition: 12, hold: 14, shape: {
      radialPhase: 2.05, secondaryPhase: 3.05, verticalPhase: 2.7, complexity: .78,
      shapeBlend: 1, brainBlend: 0, knotMix: .16, fission: .28, modeMix: .84,
      modeFrequency: 11, modePhase: 2.8, splitPhase: 3.7,
      swellCenters: [1.85, 4.1, 5.8], swellAmplitudes: [.15, .08, .12]
    } },
    { transition: 12, hold: 14, shape: {
      radialPhase: 3.1, secondaryPhase: 4.15, verticalPhase: 3.85, complexity: .84,
      shapeBlend: 1, brainBlend: 0, knotMix: .88, fission: .62, modeMix: .46,
      modeFrequency: 9, modePhase: 4.05, splitPhase: 4.75,
      swellCenters: [.55, 3.25, 4.85], swellAmplitudes: [.1, .13, .12]
    } },
    { transition: 12, hold: 12, shape: {
      radialPhase: 3.8, secondaryPhase: 5.1, verticalPhase: 4.65, complexity: .04,
      shapeBlend: 0, brainBlend: 0, knotMix: 0, fission: 0, modeMix: 0,
      modeFrequency: 7, modePhase: 0, splitPhase: 5.7,
      swellCenters: [.95, 3.28, 5.2], swellAmplitudes: [0, 0, 0]
    } }
  ];
  const shapeCycleSeconds = shapeSequence.reduce((total, stage) => total + stage.transition + stage.hold, 0);
  const shapeFields = [
    'radialPhase', 'secondaryPhase', 'verticalPhase', 'complexity', 'shapeBlend',
    'brainBlend', 'knotMix', 'fission', 'modeMix', 'modeFrequency', 'modePhase', 'splitPhase'
  ];
  function copyShape(shape) {
    return { ...shape, swellCenters: [...shape.swellCenters], swellAmplitudes: [...shape.swellAmplitudes] };
  }
  function interpolateShape(from, to, amount) {
    const result = {};
    for (const field of shapeFields) result[field] = from[field] + (to[field] - from[field]) * amount;
    result.swellCenters = to.swellCenters.map((value, index) => from.swellCenters[index] + (value - from.swellCenters[index]) * amount);
    result.swellAmplitudes = to.swellAmplitudes.map((value, index) => from.swellAmplitudes[index] + (value - from.swellAmplitudes[index]) * amount);
    return result;
  }
  function updateShapeState(seconds) {
    let remaining = ((seconds % shapeCycleSeconds) + shapeCycleSeconds) % shapeCycleSeconds;
    let previous = shapeSequence[shapeSequence.length - 1].shape;
    for (const stage of shapeSequence) {
      if (remaining < stage.transition) {
        const progress = smoothStep(0, 1, remaining / stage.transition);
        shapeState = interpolateShape(previous, stage.shape, progress);
        return;
      }
      remaining -= stage.transition;
      if (remaining < stage.hold) {
        shapeState = copyShape(stage.shape);
        return;
      }
      remaining -= stage.hold;
      previous = stage.shape;
    }
    shapeState = copyShape(shapeSequence[0].shape);
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
    const higherMode = shapeState.modeFrequency * u + shapeState.modePhase;
    const knotMix = shapeState.knotMix;
    const baseRadialKnot = (1 - knotMix) * Math.cos(third)
      + knotMix * Math.cos(fifth)
      + .29 * shapeState.fission * Math.cos(seventh);
    const baseVerticalKnot = (1 - knotMix) * Math.sin(third)
      + knotMix * Math.sin(fifth)
      + .29 * shapeState.fission * Math.sin(seventh);
    const higherModeWeight = .58 * shapeState.modeMix;
    const radialKnot = (1 - higherModeWeight) * baseRadialKnot
      + higherModeWeight * Math.cos(higherMode);
    const verticalKnot = (1 - higherModeWeight) * baseVerticalKnot
      + higherModeWeight * Math.sin(higherMode);
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
  function surfaceNormalAt(u, v, frame) {
    return normalize(add(
      scale(frame.normal, Math.cos(v)),
      scale(frame.binormal, Math.sin(v))
    ));
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
  function brainPoint3D(latitude, longitude, seconds) {
    const cosLatitude = Math.cos(latitude);
    let x = 1.48 * cosLatitude * Math.cos(longitude);
    let y = .96 * Math.sin(latitude);
    let z = .84 * cosLatitude * Math.sin(longitude);
    const fissure = Math.exp(-((z / .105) ** 2)) * cosLatitude ** 1.4;
    const broadGyri = .088 * Math.sin(7 * longitude + 1.5 * Math.sin(3 * latitude))
      + .046 * Math.cos(5 * latitude + 2.2 * Math.sin(4 * longitude));
    const fineGyri = .052 * Math.sin(15 * longitude + 2.4 * Math.sin(6 * latitude))
      + .03 * Math.cos(18 * latitude + 2.7 * Math.sin(7 * longitude));
    const breath = .012 * Math.sin(seconds * .11 + 1.5 * Math.sin(longitude * 2 + latitude));
    const texture = 1 + broadGyri + fineGyri + breath;
    const cerebellum = Math.exp(-(((x + .71) / .38) ** 2) - (((y + .52) / .31) ** 2));
    const stem = Math.exp(-(((x + .43) / .27) ** 2) - (((y + .67) / .25) ** 2) - ((z / .3) ** 2));
    const separation = .105 * Math.tanh(z / .035) * fissure;
    x *= texture * (1 + .13 * cerebellum) * (1 - .12 * stem);
    y = (y * (1 - .23 * fissure) - .12 * cerebellum - .3 * stem) * texture;
    z = (z + separation) * texture * (1 + .13 * cerebellum) * (1 - .2 * stem);
    return [x, y, z];
  }
  function brainNormalAt(latitude, longitude) {
    const point = brainPoint3D(latitude, longitude, elapsed / 1000);
    return normalize([point[0] / (1.48 * 1.48), point[1] / (.96 * .96), point[2] / (.84 * .84)]);
  }
  function drawBrain3D(seconds, yaw, pitch, roll, size, opacity) {
    if (opacity < .005) return;
    const longitudeSteps = 112;
    const latitudeSteps = 56;
    const latitudeLimit = 1.49;
    const vertices = [];
    for (let latIndex = 0; latIndex <= latitudeSteps; latIndex++) {
      const latitude = -latitudeLimit + 2 * latitudeLimit * latIndex / latitudeSteps;
      const row = [];
      for (let lonIndex = 0; lonIndex < longitudeSteps; lonIndex++) {
        const longitude = TAU * lonIndex / longitudeSteps;
        const point = brainPoint3D(latitude, longitude, seconds);
        const screen = project(point, yaw, pitch, roll, size);
        const normal = cameraPoint(brainNormalAt(latitude, longitude), yaw, pitch, roll);
        const facing = normal[2];
        row.push({ ...screen, facing, latitude, longitude });
      }
      vertices.push(row);
    }

    ctx.save();
    ctx.globalAlpha = opacity;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    // A small corrugated cerebellum and tapered brainstem complete the 3D profile.
    ctx.save();
    ctx.globalAlpha = opacity * .68;
    const cerebellumCenter = [-1.02, -.62, 0];
    const cerebellumRadii = [.4, .29, .43];
    const cerebellumPoint = (latitude, longitude) => {
      const c = Math.cos(latitude);
      const folia = 1 + .052 * Math.sin(13 * latitude + 2 * Math.sin(5 * longitude))
        + .022 * Math.sin(21 * latitude + 1.4 * Math.cos(7 * longitude));
      return [
        cerebellumCenter[0] + cerebellumRadii[0] * c * Math.cos(longitude) * folia,
        cerebellumCenter[1] + cerebellumRadii[1] * Math.sin(latitude) * folia,
        cerebellumCenter[2] + cerebellumRadii[2] * c * Math.sin(longitude) * folia
      ];
    };
    ctx.lineWidth = .62;
    for (let ring = 1; ring < 9; ring++) {
      const latitude = -1.25 + 2.5 * ring / 9;
      ctx.beginPath();
      let open = false;
      for (let step = 0; step <= 48; step++) {
        const longitude = TAU * step / 48;
        const point = cerebellumPoint(latitude, longitude);
        const projected = project(point, yaw, pitch, roll, size);
        const normal = cameraPoint(normalize([
          Math.cos(latitude) * Math.cos(longitude) / cerebellumRadii[0],
          Math.sin(latitude) / cerebellumRadii[1],
          Math.cos(latitude) * Math.sin(longitude) / cerebellumRadii[2]
        ]), yaw, pitch, roll);
        if (normal[2] > -.04) {
          if (!open) ctx.moveTo(projected.x, projected.y); else ctx.lineTo(projected.x, projected.y);
          open = true;
        } else open = false;
      }
      ctx.strokeStyle = 'rgba(119,189,243,.48)';
      ctx.stroke();
    }
    for (let meridian = 0; meridian < 40; meridian += 4) {
      const longitude = TAU * meridian / 40;
      ctx.beginPath();
      let open = false;
      for (let step = 0; step <= 20; step++) {
        const latitude = -1.42 + 2.84 * step / 20;
        const point = cerebellumPoint(latitude, longitude);
        const projected = project(point, yaw, pitch, roll, size);
        const normal = cameraPoint(normalize([
          Math.cos(latitude) * Math.cos(longitude) / cerebellumRadii[0],
          Math.sin(latitude) / cerebellumRadii[1],
          Math.cos(latitude) * Math.sin(longitude) / cerebellumRadii[2]
        ]), yaw, pitch, roll);
        if (normal[2] > -.04) {
          if (!open) ctx.moveTo(projected.x, projected.y); else ctx.lineTo(projected.x, projected.y);
          open = true;
        } else open = false;
      }
      ctx.strokeStyle = 'rgba(119,189,243,.42)';
      ctx.stroke();
    }

    const stemRings = 13;
    const stemAngles = 32;
    const stemCenter = t => [-.4 + .07 * t, -.8 - .58 * t, 0];
    const stemRadius = t => [.17 * (1 - .38 * t), .14 * (1 - .42 * t)];
    ctx.lineWidth = .68;
    for (let ring = 0; ring <= stemRings; ring++) {
      const t = ring / stemRings;
      const [radiusX, radiusZ] = stemRadius(t);
      const center = stemCenter(t);
      ctx.beginPath();
      let open = false;
      for (let step = 0; step <= stemAngles; step++) {
        const angle = TAU * step / stemAngles;
        const point = [center[0] + radiusX * Math.cos(angle), center[1], center[2] + radiusZ * Math.sin(angle)];
        const projected = project(point, yaw, pitch, roll, size);
        const normal = cameraPoint(normalize([Math.cos(angle), .12, Math.sin(angle)]), yaw, pitch, roll);
        if (normal[2] > -.04) {
          if (!open) ctx.moveTo(projected.x, projected.y); else ctx.lineTo(projected.x, projected.y);
          open = true;
        } else open = false;
      }
      ctx.strokeStyle = 'rgba(128,197,248,.48)';
      ctx.stroke();
    }
    for (let meridian = 0; meridian < stemAngles; meridian += 4) {
      const angle = TAU * meridian / stemAngles;
      ctx.beginPath();
      let open = false;
      for (let ring = 0; ring <= stemRings; ring++) {
        const t = ring / stemRings;
        const [radiusX, radiusZ] = stemRadius(t);
        const center = stemCenter(t);
        const point = [center[0] + radiusX * Math.cos(angle), center[1], center[2] + radiusZ * Math.sin(angle)];
        const projected = project(point, yaw, pitch, roll, size);
        const normal = cameraPoint(normalize([Math.cos(angle), .12, Math.sin(angle)]), yaw, pitch, roll);
        if (normal[2] > -.04) {
          if (!open) ctx.moveTo(projected.x, projected.y); else ctx.lineTo(projected.x, projected.y);
          open = true;
        } else open = false;
      }
      ctx.strokeStyle = 'rgba(128,197,248,.42)';
      ctx.stroke();
    }
    ctx.restore();

    // Draw meridians and latitude arcs only where the surface faces the camera.
    ctx.lineWidth = .68;
    for (let latIndex = 2; latIndex < latitudeSteps - 1; latIndex += 2) {
      ctx.beginPath();
      let open = false;
      for (let lonIndex = 0; lonIndex <= longitudeSteps; lonIndex++) {
        const point = vertices[latIndex][lonIndex % longitudeSteps];
        if (point.facing > -.08) {
          if (!open) ctx.moveTo(point.x, point.y); else ctx.lineTo(point.x, point.y);
          open = true;
        } else open = false;
      }
      ctx.strokeStyle = latIndex % 8 === 0 ? 'rgba(158,218,255,.54)' : 'rgba(135,199,250,.34)';
      ctx.stroke();
    }
    ctx.lineWidth = .52;
    for (let lonIndex = 0; lonIndex < longitudeSteps; lonIndex += 4) {
      ctx.beginPath();
      let open = false;
      for (let latIndex = 1; latIndex < latitudeSteps; latIndex++) {
        const point = vertices[latIndex][lonIndex];
        if (point.facing > -.08) {
          if (!open) ctx.moveTo(point.x, point.y); else ctx.lineTo(point.x, point.y);
          open = true;
        } else open = false;
      }
      ctx.strokeStyle = lonIndex % 16 === 0 ? 'rgba(116,183,241,.48)' : 'rgba(128,191,242,.32)';
      ctx.stroke();
    }

    ctx.beginPath();
    for (let latIndex = 1; latIndex < latitudeSteps; latIndex += 2) {
      for (let lonIndex = 0; lonIndex < longitudeSteps; lonIndex += 2) {
        const a = vertices[latIndex][lonIndex];
        const b = vertices[latIndex + 1][(lonIndex + 1) % longitudeSteps];
        if ((a.facing + b.facing) * .5 > .06) {
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
        }
      }
    }
    ctx.lineWidth = .36;
    ctx.strokeStyle = 'rgba(108,174,232,.2)';
    ctx.stroke();

    const nodes = [];
    for (let latIndex = 1; latIndex < latitudeSteps; latIndex += 2) {
      for (let lonIndex = 0; lonIndex < longitudeSteps; lonIndex += 2) {
        const point = vertices[latIndex][lonIndex];
        if (point.facing > -.02) nodes.push(point);
      }
    }
    nodes.sort((a, b) => a.z - b.z);
    for (const point of nodes) {
      const lighting = .48 + .48 * Math.max(0, point.facing);
      ctx.globalAlpha = opacity * (.34 + .44 * lighting);
      ctx.fillStyle = `rgba(${Math.round(90 + 44 * lighting)},${Math.round(181 + 49 * lighting)},255,.9)`;
      ctx.beginPath();
      ctx.arc(point.x, point.y, .42 + .22 * lighting, 0, TAU);
      ctx.fill();
    }

    for (let light = 0; light < 19; light++) {
      const travel = (seconds / 18 + light / 19) % 1;
      const longitude = travel * TAU;
      const lane = -0.58 + 1.16 * ((light * 7) % 19) / 18;
      const latitude = lane + .035 * Math.sin(seconds * .12 + light * .7);
      const current = project(brainPoint3D(latitude, longitude, seconds), yaw, pitch, roll, size);
        const normal = cameraPoint(brainNormalAt(latitude, longitude), yaw, pitch, roll);
      if (normal[2] < -.12) continue;
      const previous = project(brainPoint3D(latitude, longitude - .1, seconds), yaw, pitch, roll, size);
      const flicker = random01(light, Math.floor(seconds * (1.15 + light % 4 * .13)) + 19) > .23;
      const intensity = flicker ? .34 + .66 * (.5 + .5 * Math.sin(seconds * (2 + light % 5 * .47) + light)) : .13;
      ctx.globalAlpha = opacity * intensity;
      ctx.strokeStyle = 'rgba(95,255,235,.56)';
      ctx.lineWidth = 1.25;
      ctx.beginPath();
      ctx.moveTo(previous.x, previous.y);
      ctx.lineTo(current.x, current.y);
      ctx.stroke();
      const radius = 5.5 + 2.5 * intensity;
      const glow = ctx.createRadialGradient(current.x, current.y, 0, current.x, current.y, radius);
      glow.addColorStop(0, `rgba(239,255,252,${.9 * intensity})`);
      glow.addColorStop(.24, `rgba(103,255,237,${.66 * intensity})`);
      glow.addColorStop(1, 'rgba(65,221,221,0)');
      ctx.fillStyle = glow;
      ctx.beginPath();
      ctx.arc(current.x, current.y, radius, 0, TAU);
      ctx.fill();
      ctx.globalAlpha = opacity * (.62 + .38 * intensity);
      ctx.fillStyle = '#effffb';
      ctx.beginPath();
      ctx.arc(current.x, current.y, 1.2 + intensity, 0, TAU);
      ctx.fill();
    }
    ctx.restore();
  }
  function drawFusionMesh(vertices, uCount, vSteps, uSteps, opacity) {
    if (opacity < .01) return;
    const index = (u, v) => ((v + vSteps) % vSteps) * uCount + clamp(u, 0, uSteps);
    ctx.save();
    ctx.globalAlpha = opacity;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.lineWidth = .62;
    ctx.strokeStyle = 'rgba(125,211,248,.58)';
    for (let vi = 0; vi < vSteps; vi += 2) {
      ctx.beginPath();
      for (let ui = 0; ui <= uSteps; ui++) {
        const point = vertices[index(ui, vi)];
        if (ui === 0) ctx.moveTo(point.x, point.y); else ctx.lineTo(point.x, point.y);
      }
      ctx.stroke();
    }
    ctx.lineWidth = .42;
    ctx.strokeStyle = 'rgba(111,194,239,.36)';
    const ringSkip = mobile.matches ? 10 : 14;
    for (let ui = 0; ui <= uSteps; ui += ringSkip) {
      ctx.beginPath();
      for (let vi = 0; vi <= vSteps; vi++) {
        const point = vertices[index(ui, vi)];
        if (vi === 0) ctx.moveTo(point.x, point.y); else ctx.lineTo(point.x, point.y);
      }
      ctx.stroke();
    }

    // A fine point lattice keeps the changing surface legible while it pinches
    // into the two hemispheres, rather than dissolving one drawing into another.
    ctx.fillStyle = 'rgba(151,222,255,.72)';
    for (let vi = 0; vi < vSteps; vi += 2) {
      for (let ui = 0; ui <= uSteps; ui += 2) {
        const point = vertices[index(ui, vi)];
        ctx.globalAlpha = opacity * (.38 + .34 * clamp((point.z + 1.2) / 2.4));
        ctx.beginPath();
        ctx.arc(point.x, point.y, .43, 0, TAU);
        ctx.fill();
      }
    }
    ctx.restore();
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
    const n = normalize(cameraPoint(surfaceNormalAt(u, v, frame), yaw, pitch, roll));
    const depth = clamp((point[2] + 1.35) / 2.7);
    const sweep = clamp((Math.cos(u - .8) + .45 * Math.sin(v + u) + .9) / 2);
    const diffuse = .73 + .27 * Math.max(0, dot(n, lightDirection));
    const meshProgress = contourProgressAtParameter(u);
    const relativeProgress = ((meshProgress - flowProgress + .5) % 1 + 1) % 1 - .5;
    const nearestGroupProgress = Math.round(relativeProgress * groupCount) / groupCount;
    const flowDistance = Math.abs(relativeProgress - nearestGroupProgress);
    const flow = Math.exp(-.5 * (flowDistance / .024) ** 2);
    const poleDistance = Math.min(u, TAU - u);
    const capVisibility = 1 - .72 * shapeState.brainBlend * (1 - smoothStep(.035, .25, poleDistance));
    const brightness = capVisibility * (.51 + .47 * depth) * (.81 + .19 * Math.cos(v - 1.1)) * diffuse * (.96 + .08 * flow);
    const red = Math.round((69 + 66 * sweep + 28 * depth - 4 * flow) * brightness);
    const green = Math.min(255, Math.round((102 + 146 * sweep + 16 * flow) * brightness));
    const blue = Math.round((252 - 34 * sweep) * brightness);
    return {
      x: position.x, y: position.y, z: position.z,
      color: `rgba(${red},${green},${blue},${.48 + .31 * depth + .12 * flow})`,
      radius: (.35 + .2 * depth + .12 * flow) * (.72 + .28 * capVisibility)
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
    const normal = surfaceNormalAt(u, v, frame);
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
      const wrapVisibility = axon.wrapsU ? 1 - shapeState.brainBlend : 1;
      const visible = clamp((brightestFacing + .16) / .9) * wrapVisibility * (1 - shapeState.brainBlend);
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
      const visibility = clamp((soma.facing + .16) / .86) * (1 - shapeState.brainBlend);

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
    const uCount = uSteps + 1;
    const vertices = new Array(uCount * vSteps);
    const index = (u, v) => ((v + vSteps) % vSteps) * uCount + clamp(u, 0, uSteps);

    for (let vi = 0; vi < vSteps; vi++) {
      const v = TAU * vi / vSteps;
      for (let ui = 0; ui <= uSteps; ui++) {
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

    // Keep the same sampled surface as it changes from the loop into the brain.
    // The tube's circular coordinate pinches at two poles and opens into the
    // brain's folded hemispheres, so the new form grows out of the old mesh.
    const transitionBlend = smoothStep(.02, .98, shapeState.brainBlend);
    const transitionVertices = new Array(vertices.length);
    if (shapeState.brainBlend > .005 && shapeState.brainBlend < .995) {
      for (let vi = 0; vi < vSteps; vi++) {
        const v = TAU * vi / vSteps;
        const latitude = 1.49 * Math.sin(v);
        for (let ui = 0; ui <= uSteps; ui++) {
          const u = TAU * ui / uSteps;
          const source = vertices[index(ui, vi)];
          const target = project(brainPoint3D(latitude, u, seconds), yaw, pitch, roll, size);
          const amount = transitionBlend;
          transitionVertices[index(ui, vi)] = {
            x: source.x * (1 - amount) + (target.x + offsetX) * amount,
            y: source.y * (1 - amount) + (target.y + offsetY) * amount,
            z: source.z * (1 - amount) + target.z * amount
          };
        }
      }
    }

    // Three overlapping weights create a short, readable fusion phase:
    // loop -> one continuously deforming surface -> fully formed brain.
    const sourceOpacity = 1 - smoothStep(.02, .55, shapeState.brainBlend);
    const fusionOpacity = smoothStep(.02, .48, shapeState.brainBlend)
      * (1 - smoothStep(.52, .98, shapeState.brainBlend));
    const brainOpacity = smoothStep(.45, .98, shapeState.brainBlend);

    ctx.clearRect(0, 0, width, height);
    ctx.save();
    ctx.globalAlpha = sourceOpacity;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.lineWidth = .52 + .18 * shapeState.brainBlend;
    ctx.strokeStyle = `rgba(133,203,248,${.17 + .28 * shapeState.brainBlend})`;
    const capSteps = Math.round(uSteps * .01 * shapeState.brainBlend);
    for (let vi = 0; vi < vSteps; vi += 2) {
      ctx.beginPath();
      for (let ui = capSteps; ui <= uSteps - capSteps; ui++) {
        const p = vertices[index(ui, vi)];
        if (ui === capSteps) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
      }
      ctx.stroke();
    }
    ctx.lineWidth = .38 + .1 * shapeState.brainBlend;
    ctx.strokeStyle = `rgba(133,203,248,${.085 + .16 * shapeState.brainBlend})`;
    const ringSkip = mobile.matches ? 8 : 10;
    for (let ui = capSteps; ui <= uSteps - capSteps; ui += ringSkip) {
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
    ctx.restore();
    drawFusionMesh(transitionVertices, uCount, vSteps, uSteps, fusionOpacity);
    drawBrain3D(seconds, yaw, pitch, roll, size, brainOpacity);
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

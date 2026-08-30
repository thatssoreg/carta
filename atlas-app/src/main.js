import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import config from "./atlas-config.json";
import "./styles.css";

const WORLD_VIEW = { center: [5, 34], zoom: 1.65, bearing: 0, pitch: 0 };
const FRANCE_PHONE_VIEW = { center: [2.15, 46.5], zoom: 4.45, bearing: 0, pitch: 0 };
const FRANCE_BOUNDS = config.countries.france.bounds;
const TRAIL_STORAGE_KEY = "carta-atlas-rabbit-hole-v1";
const AOC_LAYERS = ["aoc-complements-fill", "aoc-areas-fill"];
const REGION_LAYERS = ["wine-region-labels", "wine-region-halos"];
const PRODUCER_LAYERS = ["producer-clusters", "producer-cluster-count", "producer-points", "producer-labels"];
const SUBJECT_REACTION_LAYERS = ["subject-areas-fill", "subject-areas-line", "subject-producer-halos", "subject-producer-labels"];

const elements = {
  intro: document.querySelector(".map-intro"),
  context: document.querySelector("[data-context]"),
  status: document.querySelector("[data-map-status]"),
  statusCopy: document.querySelector("[data-status-copy]"),
  searchForm: document.querySelector("[data-search-form]"),
  searchInput: document.querySelector("[data-search-input]"),
  searchResults: document.querySelector("[data-search-results]"),
  layersButton: document.querySelector("[data-layers-button]"),
  layerPanel: document.querySelector("[data-layer-panel]"),
  aocToggle: document.querySelector("[data-layer-aoc]"),
  igpToggle: document.querySelector("[data-layer-igp]"),
  regionsToggle: document.querySelector("[data-layer-regions]"),
  producersToggle: document.querySelector("[data-layer-producers]"),
  guidesButton: document.querySelector("[data-guides-button]"),
  discoveryPanel: document.querySelector("[data-discovery-panel]"),
  discoveryContent: document.querySelector("[data-discovery-content]"),
  rabbitButton: document.querySelector("[data-rabbit-button]"),
  rabbitCount: document.querySelector("[data-rabbit-count]"),
  rabbitDrawer: document.querySelector("[data-rabbit-drawer]"),
  rabbitTrail: document.querySelector("[data-rabbit-trail]"),
  detailPanel: document.querySelector("[data-detail-panel]"),
  detailContent: document.querySelector("[data-detail-content]"),
  backButton: document.querySelector("[data-back-detail]"),
  backLabel: document.querySelector("[data-back-label]"),
  inspectButton: document.querySelector("[data-inspect-button]"),
  sourcesDialog: document.querySelector("[data-sources-dialog]"),
  sourcesContent: document.querySelector("[data-sources-content]"),
  aboutDialog: document.querySelector("[data-about-dialog]"),
  toast: document.querySelector("[data-toast]"),
};

function readStoredTrail() {
  try {
    const value = JSON.parse(sessionStorage.getItem(TRAIL_STORAGE_KEY) || "[]");
    return Array.isArray(value) ? value.slice(-16) : [];
  } catch {
    return [];
  }
}

const state = {
  context: "world",
  franceLoaded: false,
  igpLoaded: false,
  searchIndex: null,
  atlasGuides: null,
  subjects: null,
  editorial: null,
  entryPoints: null,
  producerFeatures: null,
  searchMatches: [],
  activeSearchIndex: -1,
  activeSubjectId: null,
  activeOverlapRecords: [],
  activeMapSelection: null,
  geographicSubjectId: null,
  activeRegionPillar: "place",
  inspectMode: false,
  sourcesRendered: false,
  trail: readStoredTrail(),
};

const map = new maplibregl.Map({
  container: "map",
  style: config.basemap.styleUrl,
  ...WORLD_VIEW,
  minZoom: 1.2,
  maxZoom: 14,
  attributionControl: false,
  cooperativeGestures: true,
});

map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "bottom-right");
map.addControl(new maplibregl.AttributionControl({ compact: true }), "bottom-right");

let resolveMapReady;
const mapReady = new Promise((resolve) => { resolveMapReady = resolve; });

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function setStatus(copy, busy = false) {
  elements.statusCopy.textContent = copy;
  elements.status.classList.toggle("is-busy", busy);
}

function showToast(copy) {
  elements.toast.textContent = copy;
  elements.toast.hidden = false;
  window.clearTimeout(showToast.timer);
  showToast.timer = window.setTimeout(() => { elements.toast.hidden = true; }, 4600);
}

function prefersReducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function transitionDuration(value) {
  return prefersReducedMotion() ? 0 : value;
}

function setLayerVisibility(layerIds, visible) {
  for (const layerId of layerIds) {
    if (map.getLayer(layerId)) map.setLayoutProperty(layerId, "visibility", visible ? "visible" : "none");
  }
}

function getLabelInsertionPoint() {
  return map.getStyle().layers.find((layer) => layer.type === "symbol")?.id;
}

function addWorldLayer() {
  map.addSource("world-countries", { type: "geojson", data: config.data.countries });
  const beforeId = getLabelInsertionPoint();
  map.addLayer({
    id: "france-country-fill",
    type: "fill",
    source: "world-countries",
    filter: ["==", ["get", "carta_entity_id"], "place:france"],
    paint: {
      "fill-color": "#7f2f3f",
      "fill-opacity": ["interpolate", ["linear"], ["zoom"], 1, 0.12, 4, 0.05],
    },
  }, beforeId);
  map.addLayer({
    id: "france-country-line",
    type: "line",
    source: "world-countries",
    filter: ["==", ["get", "carta_entity_id"], "place:france"],
    paint: { "line-color": "#612331", "line-width": 1.6, "line-opacity": 0.8 },
  }, beforeId);
}

function addFranceLayers() {
  const beforeId = getLabelInsertionPoint();
  map.addSource("aoc-areas", { type: "geojson", data: config.data.aocAreas });
  map.addSource("wine-regions", { type: "geojson", data: config.data.wineRegions });
  map.addSource("producer-points", {
    type: "geojson",
    data: config.data.producerPoints,
    cluster: true,
    clusterRadius: 48,
    clusterMaxZoom: 8,
  });
  map.addSource("subject-producer-points", {
    type: "geojson",
    data: config.data.producerPoints,
  });

  map.addLayer({
    id: "aoc-areas-fill",
    type: "fill",
    source: "aoc-areas",
    minzoom: config.semanticZoom.appellationFillMin,
    filter: ["!=", ["get", "feature_type"], "geographical_complement"],
    layout: { visibility: elements.aocToggle.checked ? "visible" : "none" },
    paint: {
      "fill-color": ["case", ["==", ["get", "governance_status"], "governed"], "#7f2f3f", "#8f756f"],
      "fill-opacity": ["interpolate", ["linear"], ["zoom"], 5.15, 0.16, 8, 0.27, 11, 0.36],
      "fill-outline-color": "rgba(97, 35, 49, 0.45)",
    },
  }, beforeId);
  map.addLayer({
    id: "aoc-areas-line",
    type: "line",
    source: "aoc-areas",
    minzoom: config.semanticZoom.appellationOutlineMin,
    filter: ["!=", ["get", "feature_type"], "geographical_complement"],
    layout: { visibility: elements.aocToggle.checked ? "visible" : "none" },
    paint: {
      "line-color": ["case", ["==", ["get", "governance_status"], "governed"], "#612331", "#8c5e4e"],
      "line-width": ["interpolate", ["linear"], ["zoom"], 6, 0.45, 10, 1.1],
      "line-opacity": 0.72,
    },
  }, beforeId);
  map.addLayer({
    id: "aoc-complements-fill",
    type: "fill",
    source: "aoc-areas",
    minzoom: 8.3,
    filter: ["==", ["get", "feature_type"], "geographical_complement"],
    layout: { visibility: elements.aocToggle.checked ? "visible" : "none" },
    paint: { "fill-color": "#9a4960", "fill-opacity": 0.25, "fill-outline-color": "#723247" },
  }, beforeId);
  map.addLayer({
    id: "subject-areas-fill",
    type: "fill",
    source: "aoc-areas",
    minzoom: 4.7,
    filter: ["==", ["get", "source_feature_id"], "__none__"],
    paint: { "fill-color": "#c8a6aa", "fill-opacity": 0.34 },
  }, beforeId);
  map.addLayer({
    id: "subject-areas-line",
    type: "line",
    source: "aoc-areas",
    minzoom: 4.7,
    filter: ["==", ["get", "source_feature_id"], "__none__"],
    paint: {
      "line-color": "#713148",
      "line-width": ["interpolate", ["linear"], ["zoom"], 5, 1.8, 10, 3.4],
      "line-opacity": 0.95,
    },
  }, beforeId);
  map.addLayer({
    id: "aoc-selection-fill",
    type: "fill",
    source: "aoc-areas",
    filter: ["==", ["get", "source_feature_id"], "__none__"],
    paint: { "fill-color": "#e4975f", "fill-opacity": 0.28 },
  }, beforeId);
  map.addLayer({
    id: "aoc-selection-line",
    type: "line",
    source: "aoc-areas",
    filter: ["==", ["get", "source_feature_id"], "__none__"],
    paint: { "line-color": "#4f1724", "line-width": 3, "line-opacity": 0.95 },
  }, beforeId);
  map.addLayer({
    id: "aoc-labels",
    type: "symbol",
    source: "aoc-areas",
    minzoom: config.semanticZoom.appellationLabelMin,
    filter: ["!=", ["get", "feature_type"], "geographical_complement"],
    layout: {
      visibility: elements.aocToggle.checked ? "visible" : "none",
      "text-field": ["get", "name"],
      "text-font": ["Noto Sans Regular"],
      "text-size": 11,
      "text-padding": 3,
      "text-max-width": 10,
    },
    paint: { "text-color": "#52232e", "text-halo-color": "#fffdf8", "text-halo-width": 1.5 },
  });
  map.addLayer({
    id: "wine-region-halos",
    type: "circle",
    source: "wine-regions",
    minzoom: config.semanticZoom.wineRegionsMin,
    maxzoom: config.semanticZoom.wineRegionsMax,
    layout: { visibility: elements.regionsToggle.checked ? "visible" : "none" },
    paint: {
      "circle-radius": ["interpolate", ["linear"], ["zoom"], 4.3, 13, 7, 20],
      "circle-color": "#fffdf8",
      "circle-opacity": 0.78,
      "circle-stroke-color": "#7f2f3f",
      "circle-stroke-width": 1.4,
      "circle-stroke-opacity": 0.7,
    },
  }, beforeId);
  map.addLayer({
    id: "wine-region-labels",
    type: "symbol",
    source: "wine-regions",
    minzoom: config.semanticZoom.wineRegionsMin,
    maxzoom: config.semanticZoom.wineRegionsMax,
    layout: {
      visibility: elements.regionsToggle.checked ? "visible" : "none",
      "text-field": ["get", "name"],
      "text-font": ["Noto Sans Bold"],
      "text-size": ["interpolate", ["linear"], ["zoom"], 4.3, 12, 7, 16],
      "text-letter-spacing": 0.07,
      "text-padding": 8,
      "text-allow-overlap": true,
    },
    paint: { "text-color": "#18251f", "text-halo-color": "#fffdf8", "text-halo-width": 2 },
  });

  const producerVisibility = elements.producersToggle.checked ? "visible" : "none";
  map.addLayer({
    id: "producer-clusters",
    type: "circle",
    source: "producer-points",
    minzoom: config.semanticZoom.producerClustersMin,
    filter: ["has", "point_count"],
    layout: { visibility: producerVisibility },
    paint: {
      "circle-color": "#25312c",
      "circle-radius": ["step", ["get", "point_count"], 13, 4, 17, 10, 21],
      "circle-stroke-color": "#fffdf8",
      "circle-stroke-width": 2,
      "circle-opacity": 0.94,
    },
  }, beforeId);
  map.addLayer({
    id: "producer-cluster-count",
    type: "symbol",
    source: "producer-points",
    minzoom: config.semanticZoom.producerClustersMin,
    filter: ["has", "point_count"],
    layout: {
      visibility: producerVisibility,
      "text-field": ["get", "point_count_abbreviated"],
      "text-font": ["Noto Sans Bold"],
      "text-size": 11,
    },
    paint: { "text-color": "#fffdf8" },
  });
  map.addLayer({
    id: "producer-points",
    type: "circle",
    source: "producer-points",
    minzoom: config.semanticZoom.producerPointsMin,
    filter: ["!", ["has", "point_count"]],
    layout: { visibility: producerVisibility },
    paint: {
      "circle-radius": ["interpolate", ["linear"], ["zoom"], 8.1, 5.5, 12, 8],
      "circle-color": "#25312c",
      "circle-stroke-color": "#fffdf8",
      "circle-stroke-width": 2.2,
    },
  }, beforeId);
  map.addLayer({
    id: "producer-selection",
    type: "circle",
    source: "producer-points",
    minzoom: config.semanticZoom.producerPointsMin,
    filter: ["==", ["get", "carta_entity_id"], "__none__"],
    paint: {
      "circle-radius": 13,
      "circle-color": "rgba(0,0,0,0)",
      "circle-stroke-color": "#7f2f3f",
      "circle-stroke-width": 3,
    },
  }, beforeId);
  map.addLayer({
    id: "producer-labels",
    type: "symbol",
    source: "producer-points",
    minzoom: 9.7,
    filter: ["!", ["has", "point_count"]],
    layout: {
      visibility: producerVisibility,
      "text-field": ["get", "name"],
      "text-font": ["Noto Sans Regular"],
      "text-size": 10.5,
      "text-offset": [0, 1.35],
      "text-anchor": "top",
      "text-max-width": 12,
      "text-optional": true,
    },
    paint: { "text-color": "#18251f", "text-halo-color": "#fffdf8", "text-halo-width": 1.7 },
  });
  map.addLayer({
    id: "subject-producer-halos",
    type: "circle",
    source: "subject-producer-points",
    minzoom: config.semanticZoom.producerClustersMin,
    filter: ["==", ["get", "carta_entity_id"], "__none__"],
    paint: {
      "circle-radius": ["interpolate", ["linear"], ["zoom"], 5.6, 8, 12, 15],
      "circle-color": "#fffdf8",
      "circle-opacity": 0.9,
      "circle-stroke-color": "#7f2f3f",
      "circle-stroke-width": 2.4,
    },
  }, beforeId);
  map.addLayer({
    id: "subject-producer-labels",
    type: "symbol",
    source: "subject-producer-points",
    minzoom: 7.2,
    filter: ["==", ["get", "carta_entity_id"], "__none__"],
    layout: {
      "text-field": ["get", "name"],
      "text-font": ["Noto Sans Bold"],
      "text-size": 11,
      "text-offset": [0, 1.55],
      "text-anchor": "top",
      "text-max-width": 12,
      "text-allow-overlap": false,
    },
    paint: { "text-color": "#5d2130", "text-halo-color": "#fffdf8", "text-halo-width": 2 },
  });
}

async function ensureFranceData() {
  await mapReady;
  if (state.franceLoaded) return;
  setStatus("Loading France wine geography and stories…", true);
  addFranceLayers();
  state.franceLoaded = true;
  setStatus("France · five featured wine worlds · official AOC map");
}

async function ensureIgpData() {
  await ensureFranceData();
  if (state.igpLoaded) return;
  setStatus("Adding the broader IGP layer…", true);
  map.addSource("igp-areas", { type: "geojson", data: config.data.igpAreas });
  map.addLayer({
    id: "igp-areas-fill",
    type: "fill",
    source: "igp-areas",
    minzoom: config.semanticZoom.appellationFillMin,
    layout: { visibility: "visible" },
    paint: { "fill-color": "#486e68", "fill-opacity": 0.16, "fill-outline-color": "#365650" },
  }, getLabelInsertionPoint());
  state.igpLoaded = true;
  setStatus("France · AOC and IGP wine-area layers");
}

function panelPadding() {
  return window.matchMedia("(max-width: 720px)").matches
    ? { top: 55, right: 24, bottom: elements.detailPanel.getAttribute("aria-hidden") === "false" ? 270 : 45, left: 24 }
    : { top: 90, right: elements.detailPanel.getAttribute("aria-hidden") === "false" ? 500 : 60, bottom: 60, left: 60 };
}

async function enterFrance({ fit = true, reveal = true } = {}) {
  await ensureFranceData();
  state.context = "france";
  elements.intro.hidden = true;
  if (state.geographicSubjectId) updateContextLabel();
  else elements.context.textContent = "France";
  if (fit && window.matchMedia("(max-width: 720px)").matches) {
    map.flyTo({ ...FRANCE_PHONE_VIEW, duration: transitionDuration(1100), essential: true });
  } else if (fit) {
    map.fitBounds(FRANCE_BOUNDS, {
      padding: panelPadding(),
      maxZoom: config.countries.france.maxZoom,
      duration: transitionDuration(1100),
      essential: true,
    });
  }
  if (reveal && !state.activeSubjectId) await showDiscovery();
}

function normalizeBounds(value) {
  if (Array.isArray(value)) return value;
  try { return JSON.parse(value); } catch { return null; }
}

function captureViewport() {
  if (!map.loaded()) return null;
  const center = map.getCenter();
  return {
    center: [Number(center.lng.toFixed(6)), Number(center.lat.toFixed(6))],
    zoom: Number(map.getZoom().toFixed(4)),
    bearing: Number(map.getBearing().toFixed(2)),
    pitch: Number(map.getPitch().toFixed(2)),
  };
}

function updateContextLabel() {
  const geographic = state.subjects?.[state.geographicSubjectId];
  elements.context.textContent = geographic
    ? geographic.display_name.replace(/ AOP$/, "")
    : "France";
}

function applyViewport(viewport) {
  if (!viewport) return;
  map.easeTo({ ...viewport, padding: panelPadding(), duration: transitionDuration(720), essential: true });
}

function animateMap(action, expectedDuration) {
  return new Promise((resolve) => {
    let settled = false;
    const finish = () => {
      if (settled) return;
      settled = true;
      map.off("moveend", finish);
      window.clearTimeout(timer);
      resolve();
    };
    map.once("moveend", finish);
    const timer = window.setTimeout(finish, expectedDuration + 450);
    action();
  });
}

function mapSelectionFilter(ids) {
  return ids?.length
    ? ["match", ["get", "source_feature_id"], ids, true, false]
    : ["==", ["get", "source_feature_id"], "__none__"];
}

function applyMapSelection(selection) {
  state.activeMapSelection = selection || null;
  if (!state.franceLoaded) return;
  const areaIds = selection?.areaFeatureIds || [];
  if (map.getLayer("aoc-selection-fill")) map.setFilter("aoc-selection-fill", mapSelectionFilter(areaIds));
  if (map.getLayer("aoc-selection-line")) map.setFilter("aoc-selection-line", mapSelectionFilter(areaIds));
  const producerId = selection?.producerEntityId || "__none__";
  if (map.getLayer("producer-selection")) {
    map.setFilter("producer-selection", ["==", ["get", "carta_entity_id"], producerId]);
  }
}

function propertyMatchFilter(property, values) {
  return values?.length
    ? ["match", ["get", property], values, true, false]
    : ["==", ["get", property], "__none__"];
}

function subjectMapReaction(subject, configuredOverride = null) {
  const configured = configuredOverride || state.editorial?.subjects?.[subject?.entity_id]?.map_reaction || {};
  const areaSubjectIds = [...(configured.area_subject_ids || [])];
  const producerIds = [...(configured.producer_ids || [])];
  if (subject?.kind === "appellation" && subject.map_target && !areaSubjectIds.includes(subject.entity_id)) {
    areaSubjectIds.unshift(subject.entity_id);
  }
  if (subject?.kind === "producer" && subject.map_target && !producerIds.includes(subject.entity_id)) {
    producerIds.unshift(subject.entity_id);
  }
  if (!areaSubjectIds.length) {
    areaSubjectIds.push(...subject.connections
      .filter((connection) => connection.target_kind === "appellation" && state.subjects[connection.target_id]?.map_target)
      .slice(0, 4)
      .map((connection) => connection.target_id));
  }
  if (!producerIds.length && ["grape", "wine", "person", "project"].includes(subject?.kind)) {
    producerIds.push(...subject.connections
      .filter((connection) => connection.target_kind === "producer" && state.subjects[connection.target_id]?.map_target)
      .slice(0, 4)
      .map((connection) => connection.target_id));
  }
  const areaFeatureIds = [...new Set(areaSubjectIds.flatMap((entityId) => (
    state.subjects[entityId]?.map_target?.map_feature_ids || []
  )).filter((featureId) => featureId.startsWith("inao-")))];
  return { areaFeatureIds, producerIds: [...new Set(producerIds)] };
}

function applySubjectMapReaction(subject = null, configuredOverride = null) {
  if (!state.franceLoaded) return;
  const reaction = subject ? subjectMapReaction(subject, configuredOverride) : { areaFeatureIds: [], producerIds: [] };
  const areaFilter = propertyMatchFilter("source_feature_id", reaction.areaFeatureIds);
  const producerFilter = propertyMatchFilter("carta_entity_id", reaction.producerIds);
  if (map.getLayer("subject-areas-fill")) map.setFilter("subject-areas-fill", areaFilter);
  if (map.getLayer("subject-areas-line")) map.setFilter("subject-areas-line", areaFilter);
  if (map.getLayer("subject-producer-halos")) map.setFilter("subject-producer-halos", producerFilter);
  if (map.getLayer("subject-producer-labels")) map.setFilter("subject-producer-labels", producerFilter);
  const active = reaction.areaFeatureIds.length || reaction.producerIds.length;
  if (map.getLayer("aoc-areas-fill")) {
    map.setPaintProperty("aoc-areas-fill", "fill-opacity", active
      ? ["interpolate", ["linear"], ["zoom"], 5.15, 0.07, 8, 0.12, 11, 0.18]
      : ["interpolate", ["linear"], ["zoom"], 5.15, 0.16, 8, 0.27, 11, 0.36]);
  }
  if (map.getLayer("producer-points")) {
    map.setPaintProperty("producer-points", "circle-opacity", reaction.producerIds.length
      ? ["case", producerFilter, 1, 0.22]
      : 1);
  }
  if (map.getLayer("producer-labels")) {
    map.setPaintProperty("producer-labels", "text-opacity", reaction.producerIds.length
      ? ["case", producerFilter, 1, 0.18]
      : 1);
  }
  if (map.getLayer("producer-clusters")) {
    map.setPaintProperty("producer-clusters", "circle-opacity", reaction.producerIds.length ? 0.35 : 0.94);
  }
}

function activateRegionalPillar(pillarId, { manageDetails = true, scroll = true, syncHistory = true } = {}) {
  const subject = state.subjects?.[state.activeSubjectId];
  const editorial = state.editorial?.subjects?.[state.activeSubjectId];
  const reaction = editorial?.pillar_map_reactions?.[pillarId];
  if (!subject || !editorial?.regional_world || !reaction) return;
  state.activeRegionPillar = pillarId;
  elements.detailContent.querySelectorAll("[data-region-pillar-target]").forEach((button) => {
    const active = button.dataset.regionPillarTarget === pillarId;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-current", active ? "true" : "false");
  });
  const target = elements.detailContent.querySelector(`[data-region-pillar="${CSS.escape(pillarId)}"]`);
  if (target && manageDetails) {
    const mobile = window.matchMedia("(max-width: 720px)").matches;
    if (mobile) {
      elements.detailContent.querySelectorAll(".jura-pillar").forEach((pillar) => {
        pillar.open = pillar === target;
      });
    } else {
      target.open = true;
    }
  }
  if (target && scroll) {
    target.scrollIntoView({ behavior: prefersReducedMotion() ? "auto" : "smooth", block: "start" });
  }
  applySubjectMapReaction(subject, reaction);
  const currentStep = state.trail[state.trail.length - 1];
  if (currentStep?.subjectId === subject.entity_id) {
    currentStep.regionPillar = pillarId;
    saveTrail();
  }
  if (syncHistory && history.state?.subjectId === subject.entity_id) {
    history.replaceState({ ...history.state, regionPillar: pillarId }, "", `${location.pathname}${location.search}${subject.route}`);
  }
  const label = editorial.pillar_copy?.[pillarId]?.status
    || `${subject.display_name.replace(/ AOP$/, "")} · ${editorial.pillar_copy?.[pillarId]?.intro || "explore the map and guide together"}`;
  setStatus(label);
}

function hideDiscovery() {
  elements.discoveryPanel.hidden = true;
  elements.guidesButton.setAttribute("aria-expanded", "false");
}

function closeRabbit() {
  elements.rabbitDrawer.setAttribute("aria-hidden", "true");
  elements.rabbitDrawer.classList.remove("is-open");
  elements.rabbitButton.setAttribute("aria-expanded", "false");
}

function closeDetails({ preserveSubject = false } = {}) {
  elements.detailPanel.setAttribute("aria-hidden", "true");
  elements.detailPanel.classList.remove("is-open");
  if (!preserveSubject) state.activeSubjectId = null;
  applySubjectMapReaction(null);
  elements.backButton.hidden = true;
  renderTrail();
  if (map.loaded()) map.easeTo({ padding: { top: 0, right: 0, bottom: 0, left: 0 }, duration: transitionDuration(220) });
}

function returnToWorld({ updateHistory = true } = {}) {
  state.context = "world";
  state.activeSubjectId = null;
  state.geographicSubjectId = null;
  elements.intro.hidden = false;
  elements.context.textContent = "Orientation";
  closeDetails();
  closeSearch();
  hideDiscovery();
  closeRabbit();
  applyMapSelection(null);
  applySubjectMapReaction(null);
  map.flyTo({ ...WORLD_VIEW, duration: transitionDuration(1000), essential: true });
  setStatus("World ready · select France to begin");
  if (updateHistory) history.pushState({ subjectId: null }, "", `${location.pathname}${location.search}`);
}

async function loadExperience() {
  if (state.subjects && state.editorial && state.entryPoints && state.producerFeatures && state.atlasGuides) return;
  const [subjectResponse, editorialResponse, entryResponse, producerResponse, guideResponse] = await Promise.all([
    fetch(config.data.atlasSubjects),
    fetch(config.data.atlasEditorial),
    fetch(config.data.entryPoints),
    fetch(config.data.producerPoints),
    fetch(config.data.atlasGuides),
  ]);
  for (const response of [subjectResponse, editorialResponse, entryResponse, producerResponse, guideResponse]) {
    if (!response.ok) throw new Error(`Atlas learning data request failed (${response.status})`);
  }
  state.subjects = (await subjectResponse.json()).subjects;
  state.editorial = await editorialResponse.json();
  state.entryPoints = await entryResponse.json();
  state.producerFeatures = (await producerResponse.json()).features;
  state.atlasGuides = (await guideResponse.json()).guides;
}

function formatQuantity(quantity) {
  const value = Number(quantity.value).toLocaleString(undefined, { maximumFractionDigits: 2 });
  if (quantity.unit === "percent") return `${value}%`;
  if (quantity.unit === "ha") return `${value} ha`;
  if (quantity.unit === "km") return `${value} km`;
  return value;
}

function guideFactsMarkup(guide) {
  if (!guide) return "";
  const measured = guide.quantities.filter((item) => item.quantity.unit !== "percent").slice(0, 4);
  const shares = guide.quantities.filter((item) => item.quantity.unit === "percent").slice(0, 5);
  if (!measured.length && !shares.length) return "";
  return `
    <section class="detail-section measured-section">
      <h3>At a glance</h3>
      ${measured.length ? `<div class="fact-grid">${measured.map((item) => `
        <article class="fact-card">
          <strong>${escapeHtml(formatQuantity(item.quantity))}</strong>
          <span>${escapeHtml(item.label || item.quantity.dimension_name || item.quantity.dimension_label || item.subject_name)}</span>
          <small>${escapeHtml(item.observed_at?.slice(0, 4) || "Dated source")}</small>
        </article>`).join("")}</div>` : ""}
      ${shares.length ? `<div class="share-bars compact-shares">${shares.map((item) => `
        <div class="share-row"><div><span>${escapeHtml(item.label || item.quantity.dimension_name || item.quantity.dimension_label)}</span><strong>${escapeHtml(formatQuantity(item.quantity))}</strong></div>
        <div class="share-track" aria-hidden="true"><i style="width:${Math.max(2, Math.min(100, item.quantity.value))}%"></i></div></div>`).join("")}</div>` : ""}
    </section>`;
}

function claimLabel(claim) {
  if (claim.label) return claim.label;
  const labels = {
    identity: "The short version",
    geography: "Where it sits",
    history: "How it got here",
    genetics: "The family resemblance",
    naming: "Names to know",
    legal: "How to read the rules",
    viticulture: "In the vineyard",
    farming: "How the land is worked",
    cellar: "In the cellar",
    sensory: "In the glass",
    classification: "How it is classified",
    other: "Worth noticing",
  };
  return labels[claim.claim_type] || "Worth knowing";
}

let termInstance = 0;

function richText(value) {
  const copy = String(value || "");
  const token = /\{\{term:([a-z0-9-]+)\|([^{}]+)\}\}/g;
  let result = "";
  let cursor = 0;
  for (const match of copy.matchAll(token)) {
    result += escapeHtml(copy.slice(cursor, match.index));
    const termId = match[1];
    const label = match[2];
    const term = state.editorial?.glossary?.[termId];
    if (!term) {
      result += escapeHtml(label);
    } else {
      termInstance += 1;
      const popoverId = `term-${termId}-${termInstance}`;
      result += `<span class="inline-term">
        <button class="inline-term__trigger" type="button" aria-expanded="false" aria-controls="${popoverId}" data-term-id="${escapeHtml(termId)}">${escapeHtml(label)}<sup aria-hidden="true">?</sup></button>
        <span class="inline-term__popover" id="${popoverId}" role="note">
          <strong>${escapeHtml(term.term)}</strong>
          <span>${escapeHtml(term.definition)}</span>
          <small>${escapeHtml(term.matters)}</small>
          ${term.explore_target_id ? `<button type="button" data-explore-subject="${escapeHtml(term.explore_target_id)}">Explore this idea →</button>` : ""}
        </span>
      </span>`;
    }
    cursor = match.index + match[0].length;
  }
  result += escapeHtml(copy.slice(cursor));
  return result;
}

function signalMeta(signalId) {
  return state.editorial?.legend?.find((item) => item.id === signalId) || null;
}

function signalMarkup(signalId, { compact = false } = {}) {
  const signal = signalMeta(signalId);
  if (!signal) return "";
  return `<span class="signal signal--${escapeHtml(signalId)} ${compact ? "signal--compact" : ""}"><b aria-hidden="true">${escapeHtml(signal.symbol)}</b>${escapeHtml(signal.label)}</span>`;
}

function legendMarkup() {
  if (!state.editorial?.legend?.length) return "";
  return `<details class="signal-legend"><summary>How to read the signals</summary><div>${state.editorial.legend.map((signal) => `
    <p>${signalMarkup(signal.id, { compact: true })}<span>${escapeHtml(signal.meaning)}</span></p>`).join("")}</div></details>`;
}

function connectionNote(connection) {
  const labels = {
    GENETICALLY_CLOSE_TO: "A surprising family resemblance—not a parentage claim.",
    TRADITIONAL_IN: "One of the places where this subject has a real cultural life.",
    USED_BY: connection.direction === "outbound" ? "See who turns this grape into a working cellar language." : "One of the grapes in this producer's vocabulary.",
    MADE_FROM: connection.direction === "outbound" ? "Follow the bottle back to its grape material." : "A specific wine that lets this grape stop being abstract.",
    MADE_BY: connection.direction === "outbound" ? "Meet the maker behind this expression." : "A bottle that makes the producer's decisions visible.",
    USES_PRACTICE: connection.direction === "outbound" ? "The cellar choice that changes how this wine speaks." : "A concrete bottle in which this practice matters.",
    CLASSIFIED_AS: "Read the legal identity attached to this wine.",
    LOCATED_IN: "Open the place that gives this subject geographic context.",
    CELLAR_IN: "Find the production base without confusing it for vineyard holdings.",
    WITHIN: "See the larger place this subject belongs to.",
    WITHIN_APPELLATION: "Read the regulatory territory around this place.",
    MENTORED_BY: connection.direction === "outbound" ? "Part of the lineage: follow who taught whom." : "See how this knowledge moved to the next person.",
    WORKED_WITH: "A human collaboration that shaped the work.",
    PROFILE_COMPONENT: "A focused way to continue this subject.",
    EXPLORE: "See what this subject adds to the story.",
  };
  return labels[connection.predicate] || "Follow the relationship and see what changes.";
}

function exploreVerb(kind) {
  return kind === "producer" ? "Meet" : "Explore";
}

function mapVerb(connection) {
  if (connection.target_kind === "producer") return "Show on map";
  return `Go to ${connection.target_name.replace(/ AOP$/, "")}`;
}

function configuredFeaturedConnections(subject) {
  const configured = state.editorial?.subjects?.[subject.entity_id]?.featured_connections || [];
  const featured = configured.map((item) => ({
    ...item,
    target: state.subjects[item.target_id],
  })).filter((item) => item.target);
  const used = new Set(featured.map((item) => item.target_id));
  const fallbackPriority = { GENETICALLY_CLOSE_TO: 0, MENTORED_BY: 1, USES_PRACTICE: 2, MADE_BY: 3, MADE_FROM: 4 };
  const fallbacks = [...subject.connections]
    .filter((connection) => !used.has(connection.target_id))
    .sort((a, b) => (fallbackPriority[a.predicate] ?? 8) - (fallbackPriority[b.predicate] ?? 8) || a.target_name.localeCompare(b.target_name))
    .slice(0, Math.max(0, 3 - featured.length))
    .map((connection) => ({
      target_id: connection.target_id,
      target: state.subjects[connection.target_id],
      reason: connectionNote(connection),
      signal: connection.predicate === "GENETICALLY_CLOSE_TO" ? "rabbit-hole" : "rabbit-hole",
      action: exploreVerb(connection.target_kind),
    }));
  return [...featured, ...fallbacks].slice(0, 3);
}

function connectionGroup(kind) {
  return {
    place: "Places",
    appellation: "Wine areas",
    grape: "Grapes",
    person: "People",
    producer: "Producers",
    project: "Projects",
    wine: "Wines",
    practice: "Practices",
  }[kind] || "Unexpected connections";
}

function connectionsMarkup(subject) {
  if (!subject.connections.length) return "";
  const featured = configuredFeaturedConnections(subject);
  const featuredIds = new Set(featured.map((item) => item.target_id));
  const more = subject.connections.filter((connection) => !featuredIds.has(connection.target_id));
  const grouped = more.reduce((result, connection) => {
    const key = connectionGroup(connection.target_kind);
    (result[key] ||= []).push(connection);
    return result;
  }, {});
  return `
    ${featured.length ? `<section class="detail-section wandering-section">
      <p class="section-kicker">Where this goes next</p>
      <h3>Keep wandering</h3>
      <div class="wandering-list">${featured.map((item) => `
        <button type="button" data-explore-subject="${escapeHtml(item.target_id)}">
          <span class="wandering-copy"><strong>${escapeHtml(item.target.display_name)}</strong><small>${richText(item.reason)}</small></span>
          <span class="wandering-action">${escapeHtml(item.action || exploreVerb(item.target.kind))} <span aria-hidden="true">→</span></span>
        </button>`).join("")}</div>
    </section>` : ""}
    ${more.length ? `<details class="more-connections detail-disclosure"><summary>More connections <span>${more.length}</span></summary>
      <div class="connection-groups">${Object.entries(grouped).map(([label, connections]) => `<section><h4>${escapeHtml(label)}</h4><div>${connections.sort((a, b) => a.target_name.localeCompare(b.target_name)).map((connection) => `
        <button type="button" data-explore-subject="${escapeHtml(connection.target_id)}"><span>${escapeHtml(connection.target_name)}</span><small>${escapeHtml(connectionNote(connection))}</small><b aria-hidden="true">→</b></button>`).join("")}</div></section>`).join("")}</div>
    </details>` : ""}`;
}

function sourcesMarkup(sources) {
  const linked = sources.filter((source) => source.url);
  if (!linked.length) return "";
  return `<details class="detail-disclosure"><summary>Sources &amp; notes <span>${linked.length}</span></summary>
    <ul class="guide-sources">${linked.map((source) => `<li><a href="${escapeHtml(source.url)}" target="_blank" rel="noreferrer">${escapeHtml(source.title)}</a><small>${escapeHtml(source.publisher || "Source")}</small></li>`).join("")}</ul>
  </details>`;
}

function producerPlacement(subject) {
  const feature = state.producerFeatures?.find((item) => item.properties.carta_entity_id === subject.entity_id);
  return feature?.properties.placement_note || null;
}

function overlapMarkup(overlaps) {
  const unique = [...new Map(overlaps.map((record) => [record.source_denomination_id || record.id, record])).values()];
  if (unique.length < 2) return "";
  return `
    <section class="detail-section overlap-section">
      <h3>Wine areas sharing this point</h3>
      <p>The outlines can overlap because they govern different origins, categories, or methods. That is context, not a mapping error.</p>
      <div class="overlap-actions">${unique.slice(0, 9).map((record) => record.carta_entity_id && state.subjects[record.carta_entity_id]
        ? `<button type="button" data-go-to-subject="${escapeHtml(record.carta_entity_id)}"><span>${escapeHtml(record.name)}</span><small>${escapeHtml(record.designation || "Wine area")}</small></button>`
        : `<button type="button" data-go-to-record="${escapeHtml(record.id)}"><span>${escapeHtml(record.name)}</span><small>${escapeHtml(record.designation || "Wine area")}</small></button>`).join("")}</div>
    </section>`;
}

function contextReturnMarkup() {
  const configured = state.editorial?.context_returns || [];
  const candidates = configured.map((item) => {
    const index = [...state.trail].map((step) => step.subjectId).lastIndexOf(item.return_subject_id);
    return { ...item, index };
  }).filter((item) => (
    item.index >= 0
    && state.activeSubjectId !== item.return_subject_id
    && item.when_geographic_subject_ids.includes(state.geographicSubjectId)
  )).sort((a, b) => b.index - a.index);
  const match = candidates[0];
  return match ? `<button class="return-context" type="button" data-restore-trail="${match.index}">← ${escapeHtml(match.label)}</button>` : "";
}

function subjectEditorial(subject) {
  return state.editorial?.subjects?.[subject.entity_id] || {};
}

function subjectLead(subject) {
  return subject.claims.find((claim) => claim.claim_id === subject.lead_claim_id) || subject.claims[0] || null;
}

function mapActionMarkup(subject) {
  if (!subject.map_target) return "";
  if (state.geographicSubjectId === subject.entity_id) {
    return `<p class="current-location"><span aria-hidden="true">◎</span> You are exploring ${escapeHtml(subject.display_name.replace(/ AOP$/, ""))} on the map</p>`;
  }
  const label = subject.kind === "producer"
    ? "Show this producer base on the map"
    : `Go to ${subject.display_name.replace(/ AOP$/, "")}`;
  return `<button class="secondary-action map-action" type="button" data-go-to-current>${escapeHtml(label)} <span aria-hidden="true">↗</span></button>`;
}

function claimsMarkup(subject, claims, { heading = null, className = "" } = {}) {
  if (!claims.length) return "";
  return `${heading ? `<p class="section-kicker">${escapeHtml(heading)}</p>` : ""}${claims.map((claim) => `
    <section class="detail-section claim-section ${className} ${claim.status === "contested" ? "claim-section--note" : ""}">
      <h3>${escapeHtml(claim.status === "contested" ? "A source note" : claimLabel(claim))}</h3>
      ${claim.subject_ref !== subject.entity_id ? `<p class="claim-subject">About ${escapeHtml(claim.subject_name)}</p>` : ""}
      <p>${escapeHtml(claim.statement)}</p>
    </section>`).join("")}`;
}

function routeButtons(subject, kinds, limit = 8) {
  const routes = subject.connections.filter((connection) => kinds.includes(connection.target_kind)).slice(0, limit);
  if (!routes.length) return "";
  return `<div class="route-ledger">${routes.map((connection) => `<button type="button" data-explore-subject="${escapeHtml(connection.target_id)}"><span>${escapeHtml(connection.target_name)}</span><small>${escapeHtml(connectionNote(connection))}</small><b aria-hidden="true">→</b></button>`).join("")}</div>`;
}

function lensesMarkup(editorial) {
  const lenses = editorial.lenses || [];
  if (!lenses.length) return "";
  return `<section class="culture-panel detail-section"><p class="section-kicker">Context worth keeping</p><h3>What insiders notice</h3><div>${lenses.map((lens) => `
    <article>${lens.signal ? signalMarkup(lens.signal) : ""}<h4>${escapeHtml(lens.title)}</h4><p>${richText(lens.text)}</p>${lens.target_id && state.subjects[lens.target_id] ? `<button type="button" data-explore-subject="${escapeHtml(lens.target_id)}">Explore ${escapeHtml(state.subjects[lens.target_id].display_name)} <span aria-hidden="true">→</span></button>` : ""}</article>`).join("")}</div></section>`;
}

function stylePathsMarkup(editorial) {
  if (!editorial.style_paths?.length) return "";
  return `<section class="style-paths detail-section"><p class="section-kicker">One grape · several cellar paths</p><h3>The fork is the point</h3><div>${editorial.style_paths.map((path, index) => `
    <article><span>0${index + 1}</span><div><strong>${richText(path.name)}</strong><small>${richText(path.note)}</small></div><button type="button" aria-label="Explore ${escapeHtml(state.subjects[path.target_id].display_name)}" data-explore-subject="${escapeHtml(path.target_id)}">↗</button></article>`).join("")}</div></section>`;
}

function affinitiesMarkup(editorial) {
  if (!editorial.affinities?.length) return "";
  return `<section class="affinity-section detail-section"><p class="section-kicker">Connections worth following</p><h3>Kinship, mechanism, and Same Energy</h3><p class="affinity-intro">Each route names the specific resemblance—and keeps the differences visible.</p><div>${editorial.affinities.map((item) => {
    const target = state.subjects[item.target_id];
    return `<article>${signalMarkup(item.signal, { compact: true })}<strong>${escapeHtml(target.display_name)}</strong><small>${richText(item.reason)}</small><button type="button" aria-label="Explore ${escapeHtml(target.display_name)}" data-explore-subject="${escapeHtml(item.target_id)}">→</button></article>`;
  }).join("")}</div></section>`;
}

function regionalHeroFactsMarkup(editorial) {
  const facts = editorial.hero_facts || [];
  if (!facts.length) return "";
  return `<dl class="jura-hero-facts">${facts.map((fact) => `<div><dt>${escapeHtml(fact.label)}</dt><dd>${escapeHtml(fact.value)}</dd><small>${escapeHtml(fact.note)}</small></div>`).join("")}</dl>`;
}

function regionalPillarMarkup(id, title, intro, content, { open = false } = {}) {
  return `<details class="jura-pillar" id="region-pillar-${escapeHtml(id)}" data-region-pillar="${escapeHtml(id)}" ${open ? "open" : ""}>
    <summary data-region-pillar-summary="${escapeHtml(id)}"><span><small>${escapeHtml(intro)}</small><strong>${title}</strong></span><i aria-hidden="true">⌄</i></summary>
    <div class="jura-pillar__body">${content}</div>
  </details>`;
}

function regionalGrapesMarkup(editorial) {
  return `<div class="jura-grape-grid">${(editorial.grape_cards || []).map((card, index) => {
    const grape = state.subjects[card.target_id];
    if (!grape) return "";
    const metric = card.metric || card.share || "Know it";
    const metricLabel = card.metric_label || (card.share ? "of reported grape mix" : "regional role");
    const primary = card.primary ?? index < 2;
    return `<article class="jura-grape-card ${primary ? "is-primary" : ""}">
      <div><span>${escapeHtml(metric)}</span><small>${escapeHtml(metricLabel)}</small></div>
      <h4>${escapeHtml(grape.display_name)}</h4>
      <p>${richText(card.copy)}</p>
      <button type="button" data-explore-subject="${escapeHtml(card.target_id)}">Explore ${escapeHtml(grape.display_name)} <span aria-hidden="true">→</span></button>
    </article>`;
  }).join("")}</div>`;
}

function regionalPeopleMarkup(editorial) {
  return `<div class="jura-people-grid">${(editorial.people || []).map((person) => {
    const producer = state.subjects[person.target_id];
    if (!producer) return "";
    const mark = producer.display_name.split(/\s+/).filter((word) => word.length > 2).slice(0, 2).map((word) => word[0]).join("");
    return `<article class="jura-person-card">
      <header><span aria-hidden="true">${escapeHtml(mark)}</span><div><small>${escapeHtml(person.base)}</small><h4>${escapeHtml(producer.display_name)}</h4></div></header>
      ${person.who ? `<p class="regional-person-who"><strong>Who</strong> ${escapeHtml(person.who)}</p>` : ""}
      <p>${escapeHtml(person.reason)}</p>
      ${person.explains ? `<p class="regional-person-explains"><strong>What it explains</strong> ${escapeHtml(person.explains)}</p>` : ""}
      <ul aria-label="Key grapes, wines, and practices">${person.cues.map((cue) => `<li>${escapeHtml(cue)}</li>`).join("")}</ul>
      <div class="jura-person-actions">
        <button type="button" data-explore-subject="${escapeHtml(person.target_id)}">Explore</button>
        <button type="button" data-go-to-subject="${escapeHtml(person.target_id)}">Show on map <span aria-hidden="true">↗</span></button>
      </div>
    </article>`;
  }).join("")}</div>`;
}

function regionalAreaScaleMarkup(guide) {
  const allowed = new Set([
    "appellation:arbois",
    "appellation:l-etoile",
    "appellation:chateau-chalon",
    "appellation:cremant-du-jura",
    "appellation:macvin-du-jura",
  ]);
  const quantities = (guide?.quantities || []).filter((item) => allowed.has(item.subject_ref) && item.quantity?.measure === "claimed_vineyard_area");
  if (!quantities.length) return "";
  const max = Math.max(...quantities.map((item) => item.quantity.value));
  return `<section class="jura-area-scale"><header><p class="section-kicker">Scale, in context</p><h4>Reported claimed area</h4></header><div>${quantities.map((item) => `<div><span>${escapeHtml(item.label)}</span><i aria-hidden="true" style="--area-share:${Math.max(5, (item.quantity.value / max) * 100)}%"></i><strong>${escapeHtml(formatQuantity(item.quantity))}</strong></div>`).join("")}</div><p>2023 revendication basis. Overlapping category areas are not additive.</p></section>`;
}

function regionalStyleComparisonMarkup(editorial) {
  if (!editorial.style_comparison?.length) return "";
  return `<section class="regional-style-comparison"><header><p class="section-kicker">Same geography · different path</p><h4>Dry, sweet, and late harvest</h4></header><div>${editorial.style_comparison.map((path) => `
    <article><strong>${richText(path.label)}</strong><b>${escapeHtml(path.value)}</b><small>${richText(path.detail)}</small></article>`).join("")}</div><p>Values are fermentable-sugar thresholds in the current specification, not tasting-note promises.</p></section>`;
}

function regionalRulesMarkup(subject, guide, overlaps, editorial, ruleClaims) {
  // A world's rule grammar is authored per world. Nothing is substituted from
  // another region: a world with no rule groups of its own shows none.
  const groups = editorial.rules?.groups || [];
  const intro = editorial.rules?.intro ? `<section class="jura-rule-intro"><p>${richText(editorial.rules.intro)}</p></section>` : "";
  return `${intro}
    ${groups.length ? `<div class="jura-rule-groups">${groups.map((group) => `<section><header><h4>${escapeHtml(group.label)}</h4><p>${escapeHtml(group.note)}</p></header><div>${group.ids.filter((id) => state.subjects[id]).map((id) => {
      const target = state.subjects[id];
      return `<button type="button" data-go-to-subject="${escapeHtml(id)}"><span>${escapeHtml(target.display_name)}</span><small>Highlight on map</small><b aria-hidden="true">↗</b></button>`;
    }).join("")}</div></section>`).join("")}</div>` : ""}
    ${subject.entity_id === "place:jura" ? regionalAreaScaleMarkup(guide) : ""}
    ${claimsMarkup(subject, ruleClaims)}
    ${overlapMarkup(overlaps)}`;
}

function regionalPlaceMarkup(subject, guide, overlaps, editorial, lead, claims) {
  const landClaims = [lead, ...claims.filter((claim) => ["geography", "climate", "geology"].includes(claim.claim_type))].filter(Boolean).slice(0, 3);
  const ruleClaims = claims.filter((claim) => ["legal", "classification"].includes(claim.claim_type)).slice(0, 3);
  const story = editorial.place_story;
  const copy = editorial.pillar_copy || {};
  // Each world speaks for itself. A pillar with no authored lede stays thin
  // rather than borrowing another region's sentence as a default.
  const lede = (pillar) => (copy[pillar]?.lede ? `<p class="jura-pillar-lede">${escapeHtml(copy[pillar].lede)}</p>` : "");
  const place = `${story ? `<section class="jura-place-story"><p class="section-kicker">${escapeHtml(story.kicker)}</p><h4>${escapeHtml(story.title)}</h4><p>${richText(story.text)}</p><button type="button" data-region-map-reaction="place">${escapeHtml(story.button)}</button></section>` : ""}${claimsMarkup(subject, landClaims)}`;
  const grapes = `${lede("grapes")}${regionalStyleComparisonMarkup(editorial)}${regionalGrapesMarkup(editorial)}`;
  const people = `${lede("people")}${regionalPeopleMarkup(editorial)}`;
  const culture = `${lede("culture")}${lensesMarkup(editorial)}`;
  const rules = `${lede("rules")}${regionalRulesMarkup(subject, guide, overlaps, editorial, ruleClaims)}`;
  return `
    <nav class="chapter-nav" aria-label="${escapeHtml(subject.display_name)} guide sections">
      <button type="button" class="is-active" aria-current="true" data-region-pillar-target="place">The Place</button>
      <button type="button" aria-current="false" data-region-pillar-target="grapes">The Grapes &amp; Wines</button>
      <button type="button" aria-current="false" data-region-pillar-target="people">The People</button>
      <button type="button" aria-current="false" data-region-pillar-target="culture">The Culture</button>
      <button type="button" aria-current="false" data-region-pillar-target="rules">The Rules</button>
    </nav>
    <div class="jura-pillars">
      ${regionalPillarMarkup("place", "The Place", copy.place?.intro || "Geography · scale · physical setting", place, { open: true })}
      ${regionalPillarMarkup("grapes", "The Grapes &amp; Wines", copy.grapes?.intro || "Grapes · wines · cellar paths", grapes, { open: true })}
      ${regionalPillarMarkup("people", "The People", copy.people?.intro || "Producers · ways into the world", people, { open: true })}
      ${regionalPillarMarkup("culture", "The Culture", copy.culture?.intro || "Transmission · access · context", culture, { open: true })}
      ${regionalPillarMarkup("rules", "The Rules", copy.rules?.intro || "Origins · categories · legal paths", rules, { open: true })}
    </div>`;
}

function grapeMarkup(subject, editorial, claims) {
  const lead = subjectLead(subject);
  const culturalMachines = subject.entity_id === "grape:chardonnay" ? `<section class="cultural-machines detail-section">
    <p class="section-kicker">One organism · two regional scripts</p><h3>Same grape. Different cultural machine.</h3>
    <div><article><span>Jura</span><strong>Cellar choice stays audible</strong><p>Topped, under-veil, blended and sparkling paths coexist; the grape name does not settle the register.</p></article>
    <article><span>Burgundy</span><strong>Place hierarchy leads</strong><p>A much larger culture of nested origin makes classification and named place the primary reading frame.</p></article></div>
    ${lead ? `<p class="cultural-machines__evidence">${escapeHtml(lead.statement)}</p>` : ""}
  </section>` : "";
  return `${culturalMachines}${stylePathsMarkup(editorial)}${affinitiesMarkup(editorial)}${lensesMarkup(editorial)}${claimsMarkup(subject, claims.slice(0, 6), { heading: "What the sources let us say" })}`;
}

function appellationMarkup(subject, guide, overlaps, claims) {
  const rules = claims.filter((claim) => ["legal", "classification"].includes(claim.claim_type));
  const context = claims.filter((claim) => !["legal", "classification"].includes(claim.claim_type));
  return `<section class="territory-section detail-section"><p class="section-kicker">Territory first</p><h3>Read the outline</h3>${guideFactsMarkup(guide)}${overlapMarkup(overlaps)}</section>
    <section class="regulation-panel detail-section"><p class="section-kicker">Rules second</p><h3>What the name governs</h3>${claimsMarkup(subject, rules.length ? rules : claims.slice(0, 3))}</section>
    ${claimsMarkup(subject, context.slice(0, 3), { heading: "Life inside the outline", className: "culture-claim" })}`;
}

function humanMarkup(subject, editorial, claims) {
  const producer = subject.kind === "producer";
  return `<section class="human-ledger detail-section"><p class="section-kicker">${producer ? "Producer dossier" : "A human subject"}</p><h3>${producer ? "What this producer makes legible" : "Work, place, transmission"}</h3>${claimsMarkup(subject, claims.slice(0, 6))}${routeButtons(subject, ["person", "producer", "project", "place", "grape", "wine", "practice", "appellation"], 8)}</section>${lensesMarkup(editorial)}`;
}

function wineMarkup(subject, claims) {
  return `<section class="wine-expression detail-section"><p class="section-kicker">A specific expression</p><h3>Read the bottle outward</h3>${routeButtons(subject, ["grape", "producer", "project", "practice", "appellation"], 8)}${claimsMarkup(subject, claims.slice(0, 5))}</section>`;
}

function practiceMarkup(subject, editorial, claims) {
  return `<section class="word-study detail-section"><p class="section-kicker">Helpful vernacular</p><h3>A word that prevents a shortcut</h3><p>${richText(editorial.thesis || subjectLead(subject)?.statement || "")}</p>${routeButtons(subject, ["wine", "producer", "grape"], 7)}${claimsMarkup(subject, claims.slice(0, 3))}</section>`;
}

function subjectCardMarkup(subject, guide = null, overlaps = []) {
  const editorial = subjectEditorial(subject);
  const lead = subjectLead(subject);
  const quantitativeClaimIds = new Set((guide?.quantities || []).map((item) => item.claim_id));
  const claims = subject.claims.filter((claim) => claim !== lead && !quantitativeClaimIds.has(claim.claim_id));
  const placement = producerPlacement(subject);
  const thesis = editorial.thesis || lead?.statement || "Follow the connections out of this subject and see where they land.";
  const monogram = subject.display_name.split(/\s+/).filter((word) => word.length > 2).slice(0, 2).map((word) => word[0]).join("");
  const isRegionalWorld = Boolean(editorial.regional_world);
  let body = "";
  if (isRegionalWorld) body = regionalPlaceMarkup(subject, guide, overlaps, editorial, lead, claims);
  else if (subject.kind === "place") body = `${guideFactsMarkup(guide)}${claimsMarkup(subject, claims.slice(0, 6))}${routeButtons(subject, ["appellation", "grape", "producer"], 10)}`;
  else if (subject.kind === "appellation") body = appellationMarkup(subject, guide, overlaps, claims);
  else if (subject.kind === "grape") body = grapeMarkup(subject, editorial, claims);
  else if (["producer", "person", "project"].includes(subject.kind)) body = humanMarkup(subject, editorial, claims);
  else if (subject.kind === "wine") body = wineMarkup(subject, claims);
  else if (subject.kind === "practice") body = practiceMarkup(subject, editorial, claims);
  else body = claimsMarkup(subject, claims.slice(0, 6));
  return `<article class="subject-card subject-card--${escapeHtml(subject.kind)} ${isRegionalWorld ? "subject-card--regional-world" : ""}">
    ${contextReturnMarkup()}
    <header class="subject-hero">
      ${["producer", "person", "project"].includes(subject.kind) ? `<span class="subject-monogram" aria-hidden="true">${escapeHtml(monogram)}</span>` : ""}
      <p class="detail-eyebrow">${escapeHtml(editorial.hero_kicker || subject.kind_label)}</p>
      <h2>${escapeHtml(subject.display_name)}</h2>
      ${placement ? `<p class="subject-place">${escapeHtml(placement)}</p>` : ""}
      <p class="guide-lede">${richText(thesis)}</p>
      ${isRegionalWorld ? regionalHeroFactsMarkup(editorial) : ""}
      ${mapActionMarkup(subject)}
      ${isRegionalWorld ? "" : legendMarkup()}
    </header>
    ${body}
    ${connectionsMarkup(subject)}
    ${sourcesMarkup(subject.sources)}
  </article>`;
}

function mapCoverageMarkup(record, overlaps = []) {
  const isRegion = record.feature_type === "wine_region_orientation" || record.result_type === "wine_region";
  const designation = isRegion ? "Wine-region guide" : `${record.designation || "Wine"} map area`;
  const sourceMeaning = isRegion
    ? "This guide mark is derived from mapped child-appellation areas for orientation. It is not a statutory region boundary."
    : "This shape is INAO's cartographic representation of a regulatory geographical area. It is not a map of approved vineyard parcels or planted vines.";
  return `
    <p class="detail-eyebrow">${escapeHtml(designation)}</p>
    <h2>${escapeHtml(record.name)}</h2>
    <p class="guide-lede">This outline is the official production area — its legal shape, drawn by the rules. What grows inside it, and who farms it, is a separate question. Compare it with the areas it touches.</p>
    <button class="secondary-action" type="button" data-go-to-record="${escapeHtml(record.id)}">Go to this area</button>
    ${overlapMarkup(overlaps)}
    <details class="detail-disclosure"><summary>What this shape means</summary><p>${escapeHtml(sourceMeaning)}</p></details>`;
}

function renderPanelMarkup(markup) {
  elements.detailContent.innerHTML = markup;
  elements.detailContent.scrollTop = 0;
  const mobile = window.matchMedia("(max-width: 720px)").matches;
  elements.detailContent.querySelectorAll(".jura-pillar").forEach((pillar) => {
    pillar.open = !mobile || pillar.dataset.regionPillar === "place";
  });
}

function openPanel(markup) {
  elements.detailPanel.setAttribute("aria-hidden", "false");
  elements.detailPanel.classList.add("is-open");
  renderPanelMarkup(markup);
  map.easeTo({ padding: panelPadding(), duration: transitionDuration(300) });
}

function saveTrail() {
  sessionStorage.setItem(TRAIL_STORAGE_KEY, JSON.stringify(state.trail.slice(-16)));
  renderTrail();
}

function recordTrail(subject, { moved = false } = {}) {
  const last = state.trail[state.trail.length - 1];
  const geographic = state.subjects?.[state.geographicSubjectId] || null;
  const step = {
    subjectId: subject.entity_id,
    label: subject.display_name,
    route: subject.route,
    viewport: captureViewport(),
    mapTarget: moved ? subject.map_target : null,
    contextMapTarget: geographic?.map_target || null,
    selection: state.activeMapSelection,
    geographicSubjectId: state.geographicSubjectId,
    regionPillar: state.editorial?.subjects?.[subject.entity_id]?.regional_world ? state.activeRegionPillar : null,
  };
  if (last?.subjectId === step.subjectId) state.trail[state.trail.length - 1] = step;
  else state.trail.push(step);
  state.trail = state.trail.slice(-16);
  saveTrail();
}

function renderTrail() {
  const count = state.trail.length;
  elements.rabbitCount.hidden = count === 0;
  elements.rabbitCount.textContent = String(count);
  elements.rabbitTrail.innerHTML = count
    ? state.trail.map((step, index) => `<li class="${step.subjectId === state.activeSubjectId ? "is-current" : ""}"><button type="button" data-restore-trail="${index}"><span>${escapeHtml(step.label)}</span><small>${step.subjectId === state.activeSubjectId ? "Here now" : "Return to this view"}</small></button></li>`).join("")
    : '<li class="rabbit-empty">Your trail will appear as soon as something catches your eye.</li>';
}

function historyStateFor(subject, fromSubjectId = history.state?.fromSubjectId || null) {
  return {
    subjectId: subject.entity_id,
    fromSubjectId,
    viewport: captureViewport(),
    selection: state.activeMapSelection,
    geographicSubjectId: state.geographicSubjectId,
    regionPillar: state.editorial?.subjects?.[subject.entity_id]?.regional_world ? state.activeRegionPillar : null,
    panelOpen: true,
  };
}

function setHistory(subject, mode, fromSubjectId = null) {
  if (mode === "none") return;
  const method = mode === "replace" ? "replaceState" : "pushState";
  const origin = mode === "replace" ? history.state?.fromSubjectId || fromSubjectId : fromSubjectId;
  history[method](historyStateFor(subject, origin), "", `${location.pathname}${location.search}${subject.route}`);
}

function updateBackButton(currentState = history.state) {
  const previous = state.subjects?.[currentState?.fromSubjectId];
  elements.backButton.hidden = !previous;
  elements.backLabel.textContent = previous ? `Back to ${previous.display_name}` : "Back";
}

async function moveToMapTarget(subject, { selection = null } = {}) {
  const target = subject.map_target;
  if (!target) return false;
  await enterFrance({ fit: false, reveal: false });
  state.geographicSubjectId = subject.entity_id;
  if (target.kind === "bounds") {
    const areaFeatureIds = target.map_feature_ids.filter((id) => id.startsWith("inao-"));
    applyMapSelection(selection || { areaFeatureIds, producerEntityId: null });
    const duration = transitionDuration(900);
    await animateMap(() => map.fitBounds(target.bounds, {
      padding: panelPadding(),
      maxZoom: target.max_zoom,
      duration,
      essential: true,
    }), duration);
  } else if (target.kind === "point") {
    applyMapSelection(selection || { areaFeatureIds: [], producerEntityId: subject.entity_id });
    const duration = transitionDuration(900);
    await animateMap(() => map.flyTo({
      center: target.center,
      zoom: target.zoom,
      padding: panelPadding(),
      duration,
      essential: true,
    }), duration);
  }
  if (subject.entity_id === "appellation:jurancon") {
    const cameFromJura = state.trail.some((step) => ["place:jura", "grape:savagnin"].includes(step.subjectId));
    showToast(cameFromJura ? "You've wandered from Jura to the western Pyrenees." : "Jurançon · one geography, several wine paths.");
  }
  return true;
}

async function navigateSubject(entityId, {
  moveMap = false,
  historyMode = "push",
  addTrail = true,
  restore = null,
  overlaps = [],
} = {}) {
  try {
    await loadExperience();
    const subject = state.subjects[entityId];
    if (!subject) throw new Error(`No native subject for ${entityId}`);
    const previousSubjectId = state.activeSubjectId && state.activeSubjectId !== entityId
      ? state.activeSubjectId
      : history.state?.subjectId && history.state.subjectId !== entityId
        ? history.state.subjectId
        : history.state?.fromSubjectId || null;
    await enterFrance({ fit: false, reveal: false });
    hideDiscovery();
    closeRabbit();
    state.activeSubjectId = entityId;
    state.activeOverlapRecords = overlaps;
    if (restore?.geographicSubjectId) {
      state.geographicSubjectId = restore.geographicSubjectId;
    } else if (moveMap && subject.map_target) {
      state.geographicSubjectId = subject.entity_id;
    }
    const guide = state.atlasGuides[entityId] || null;
    openPanel(subjectCardMarkup(subject, guide, overlaps));
    let moved = false;
    const restoredGeographic = restore?.geographicSubjectId
      ? state.subjects[restore.geographicSubjectId]
      : null;
    if (restore && restoredGeographic?.map_target) {
      moved = await moveToMapTarget(restoredGeographic, { selection: restore.selection || null });
    } else if (restore?.mapTarget) {
      moved = await moveToMapTarget(subject, { selection: restore.selection || null });
    } else if (restore?.viewport) {
      state.geographicSubjectId = restore.geographicSubjectId || null;
      applyMapSelection(restore.selection || null);
      applyViewport(restore.viewport);
    } else if (moveMap) {
      moved = await moveToMapTarget(subject);
    }
    applySubjectMapReaction(subject);
    if (state.editorial?.subjects?.[subject.entity_id]?.regional_world) {
      activateRegionalPillar(restore?.regionPillar || "place", { manageDetails: true, scroll: false, syncHistory: false });
    } else {
      setStatus(`${subject.display_name.replace(/ AOP$/, "")} · explore the guide and map together`);
    }
    if (addTrail) recordTrail(subject, { moved });
    else renderTrail();
    setHistory(subject, historyMode, previousSubjectId);
    updateBackButton(historyMode === "none" ? restore || history.state : history.state);
    updateContextLabel();
  } catch (error) {
    console.error(error);
    showToast("That path could not open. The map is still ready.");
  }
}

async function restoreTrailStep(index) {
  const step = state.trail[index];
  if (!step) return;
  await navigateSubject(step.subjectId, {
    moveMap: false,
    historyMode: "push",
    addTrail: false,
    restore: step,
  });
  if (step.subjectId === "grape:savagnin") showToast("Back to Savagnin, with the map exactly where you left it.");
  if (step.subjectId === "grape:petit-manseng") showToast("Back to Petit Manseng, with the map exactly where you left it.");
}

async function showDiscovery() {
  try {
    await loadExperience();
    elements.discoveryContent.innerHTML = `
      <div class="featured-worlds" aria-label="Featured wine worlds">${state.entryPoints.featured_worlds.map((world) => `
        <button type="button" data-go-to-subject="${escapeHtml(world.entity_id)}"><span>${escapeHtml(world.name)}</span><small>Guide</small></button>`).join("")}</div>
      <div class="entry-grid">${state.entryPoints.entry_points.map((entry) => `
        <button class="entry-card" type="button" data-entry-subject="${escapeHtml(entry.subject_id)}">
          <small>${escapeHtml(entry.kicker)}</small>
          <strong>${escapeHtml(entry.title)}</strong>
          <span>Follow this thread →</span>
        </button>`).join("")}</div>`;
    elements.discoveryPanel.hidden = false;
    elements.guidesButton.setAttribute("aria-expanded", "true");
  } catch {
    showToast("The questions could not load. Search and the map remain available.");
  }
}

async function loadSearchIndex() {
  if (!state.searchIndex) {
    const response = await fetch(config.data.searchIndex);
    if (!response.ok) throw new Error(`Search index request failed (${response.status})`);
    state.searchIndex = await response.json();
  }
  return state.searchIndex;
}

function searchScore(record, query) {
  const name = record.name.toLocaleLowerCase();
  if (name === query) return 0;
  if (name.startsWith(query)) return 1;
  if (name.split(/\s+/).some((word) => word.startsWith(query))) return 2;
  return 3;
}

function searchResultLabel(record) {
  if (record.result_type === "native_subject") {
    const kind = { grape: "Grape", producer: "Producer", wine: "Wine", practice: "Cellar practice", place: "Place", appellation: "Wine area" }[record.subject_kind] || "Explore";
    return `${kind}${record.context_label ? ` · ${record.context_label}` : ""}`;
  }
  if (record.result_type === "wine_region") return "Region · Guide";
  return `${record.designation || "Wine area"} · ${record.experience_level === "native_guide" ? "Guide + map" : "Official map"}`;
}

async function renderSearch() {
  const query = elements.searchInput.value.trim().toLocaleLowerCase();
  if (query.length < 2) { closeSearch(); return; }
  try {
    const records = await loadSearchIndex();
    state.searchMatches = records
      .filter((record) => `${record.name} ${record.context_label || ""}`.toLocaleLowerCase().includes(query))
      .sort((a, b) => searchScore(a, query) - searchScore(b, query) || a.name.localeCompare(b.name))
      .slice(0, 12);
    state.activeSearchIndex = state.searchMatches.length ? 0 : -1;
    elements.searchResults.innerHTML = state.searchMatches.length
      ? state.searchMatches.map((record, index) => `
          <button id="search-option-${index}" type="button" role="option" aria-selected="${index === 0}" data-result-index="${index}">
            <span>${escapeHtml(record.name)}</span>
            <small>${escapeHtml(searchResultLabel(record))}</small>
          </button>`).join("")
      : `<p class="search-empty">No place, grape, or producer matches “${escapeHtml(elements.searchInput.value.trim())}”.</p>`;
    elements.searchResults.hidden = false;
    elements.searchInput.setAttribute("aria-expanded", "true");
    if (state.activeSearchIndex >= 0) elements.searchInput.setAttribute("aria-activedescendant", "search-option-0");
  } catch {
    showToast("Search could not load. The map remains available.");
  }
}

function closeSearch() {
  elements.searchResults.hidden = true;
  elements.searchInput.setAttribute("aria-expanded", "false");
  elements.searchInput.removeAttribute("aria-activedescendant");
  state.activeSearchIndex = -1;
}

async function openMapRecord(record, overlaps = [], { focus = true } = {}) {
  await enterFrance({ fit: false, reveal: false });
  hideDiscovery();
  state.activeSubjectId = null;
  state.activeOverlapRecords = overlaps;
  openPanel(mapCoverageMarkup(record, overlaps));
  if (focus) {
    const bounds = normalizeBounds(record.bounds);
    if (bounds) {
      applyMapSelection({ areaFeatureIds: record.source_feature_ids || [], producerEntityId: null });
      map.fitBounds(bounds, { padding: panelPadding(), maxZoom: record.result_type === "wine_region" ? 7.4 : 10.4, duration: transitionDuration(850), essential: true });
    }
  }
}

async function selectSearchResult(index) {
  const record = state.searchMatches[index];
  if (!record) return;
  closeSearch();
  elements.searchInput.value = record.name;
  if (record.native_route && record.carta_entity_id) {
    const shouldMove = ["aoc_appellation", "igp_appellation", "wine_region"].includes(record.result_type);
    await navigateSubject(record.carta_entity_id, { moveMap: shouldMove });
  } else {
    await openMapRecord(record, [], { focus: true });
  }
}

function updateActiveSearch(nextIndex) {
  if (!state.searchMatches.length) return;
  state.activeSearchIndex = (nextIndex + state.searchMatches.length) % state.searchMatches.length;
  elements.searchResults.querySelectorAll("[role='option']").forEach((option, index) => option.setAttribute("aria-selected", String(index === state.activeSearchIndex)));
  const active = elements.searchResults.querySelector(`[data-result-index="${state.activeSearchIndex}"]`);
  elements.searchInput.setAttribute("aria-activedescendant", active.id);
  active.scrollIntoView({ block: "nearest" });
}

function featureRecord(feature) {
  return feature?.properties ?? feature ?? {};
}

async function searchRecordForFeature(feature) {
  const properties = featureRecord(feature);
  const records = await loadSearchIndex();
  if (properties.feature_type === "wine_region_orientation") {
    return records.find((record) => record.id === properties.source_feature_id);
  }
  return records.find((record) => record.source_denomination_id === properties.source_denomination_id);
}

function distanceKm(a, b) {
  const toRadians = (value) => value * Math.PI / 180;
  const earth = 6371;
  const dLat = toRadians(b[1] - a[1]);
  const dLon = toRadians(b[0] - a[0]);
  const lat1 = toRadians(a[1]);
  const lat2 = toRadians(b[1]);
  const value = Math.sin(dLat / 2) ** 2 + Math.sin(dLon / 2) ** 2 * Math.cos(lat1) * Math.cos(lat2);
  return 2 * earth * Math.asin(Math.sqrt(value));
}

async function inspectPoint(event) {
  await loadExperience();
  const layers = AOC_LAYERS.filter((layer) => map.getLayer(layer) && map.getLayoutProperty(layer, "visibility") !== "none");
  if (state.igpLoaded && map.getLayoutProperty("igp-areas-fill") !== "none") layers.push("igp-areas-fill");
  const features = map.queryRenderedFeatures(event.point, { layers });
  const unique = [...new Map(features.map((feature) => [feature.properties.source_denomination_id || feature.id, feature])).values()];
  const records = (await Promise.all(unique.map((feature) => searchRecordForFeature(feature)))).filter(Boolean);
  const regionalWorld = Object.entries(state.editorial?.subjects || {})
    .filter(([, editorial]) => editorial.regional_world)
    .map(([entityId, editorial]) => ({ subject: state.subjects[entityId], editorial }))
    .find(({ editorial }) => records.some((record) => (
      editorial.map_reaction?.area_subject_ids || []
    ).includes(record.carta_entity_id)));
  const grapes = regionalWorld
    ? (regionalWorld.editorial.grape_cards || []).map((card) => ({ target_id: card.target_id, target_name: state.subjects[card.target_id]?.display_name })).filter((item) => item.target_name)
    : [];
  const point = [event.lngLat.lng, event.lngLat.lat];
  const nearby = (state.producerFeatures || [])
    .map((feature) => ({ feature, distance: distanceKm(point, feature.geometry.coordinates) }))
    .filter((item) => item.distance <= 45)
    .sort((a, b) => a.distance - b.distance)
    .slice(0, 4);
  setInspectMode(false);
  const areasMarkup = records.length
    ? `<div class="inspection-list">${records.map((record) => record.carta_entity_id && state.subjects[record.carta_entity_id]
      ? `<button type="button" data-go-to-subject="${escapeHtml(record.carta_entity_id)}"><span>${escapeHtml(record.name)}</span><small>${escapeHtml(record.designation || "Wine area")}</small></button>`
      : `<button type="button" data-go-to-record="${escapeHtml(record.id)}"><span>${escapeHtml(record.name)}</span><small>${escapeHtml(record.designation || "Official map")}</small></button>`).join("")}</div>`
    : '<p class="inspection-empty">No visible wine-area shape covers this exact point at the current zoom. Try again inside one of the shaded areas.</p>';
  const grapesMarkup = grapes.length
    ? `<section class="detail-section"><h3>Grapes to know in this context</h3><div class="topic-pills">${grapes.map((grape) => `<button type="button" data-explore-subject="${escapeHtml(grape.target_id)}">${escapeHtml(grape.target_name)}</button>`).join("")}</div></section>`
    : "";
  const producersMarkup = nearby.length
    ? `<section class="detail-section"><h3>Producer bases nearby</h3><div class="inspection-list">${nearby.map(({ feature, distance }) => `<button type="button" data-explore-subject="${escapeHtml(feature.properties.carta_entity_id)}"><span>${escapeHtml(feature.properties.name)}</span><small>${escapeHtml(feature.properties.place_label)} · about ${Math.max(1, Math.round(distance))} km</small></button>`).join("")}</div><p class="inspection-note">Distances are straight-line orientation only. Markers show production bases, not vineyards.</p></section>`
    : "";
  openPanel(`
    <p class="detail-eyebrow">What am I looking at?</p>
    <h2>${regionalWorld ? `A point in ${escapeHtml(regionalWorld.subject.display_name)}’s wine world` : "A point on the wine map"}</h2>
    <p class="guide-lede">${regionalWorld ? "A legal outline, a producer's base and the region's own argument can all meet at one point. They are three different kinds of statement, and this panel keeps them apart." : "What the visible wine areas can tell you about this exact point."}</p>
    <section class="detail-section"><h3>Wine areas covering this point</h3>${areasMarkup}</section>
    ${grapesMarkup}
    ${producersMarkup}
    ${regionalWorld ? `<section class="detail-section inspection-why"><h3>What this point is arguing about</h3><p>${richText(regionalWorld.editorial.thesis)}</p></section>` : ""}
    <details class="detail-disclosure technical-disclosure"><summary>Point details</summary><p>Selected at ${event.lngLat.lat.toFixed(4)}, ${event.lngLat.lng.toFixed(4)}. This click is a map query, not a municipality claim.</p></details>`);
}

function setInspectMode(active) {
  state.inspectMode = active;
  elements.inspectButton.setAttribute("aria-pressed", String(active));
  elements.inspectButton.classList.toggle("is-active", active);
  map.getCanvas().classList.toggle("is-inspecting", active);
  if (active) {
    setStatus("Inspection on · choose a point inside the wine areas");
    showToast("Choose a point. We'll unpack every visible wine area covering it.");
  } else if (state.context === "france") {
    const place = state.subjects?.[state.geographicSubjectId]?.display_name.replace(/ AOP$/, "") || "France";
    setStatus(`${place} · explore a guide, a grape, or a producer`);
  }
}

async function handleMapClick(event) {
  if (state.context === "world") {
    const france = map.queryRenderedFeatures(event.point, { layers: ["france-country-fill"] });
    if (france.length) await enterFrance();
    return;
  }
  if (state.inspectMode) {
    await inspectPoint(event);
    return;
  }
  const producerLayers = ["producer-clusters", "producer-points"].filter((layer) => map.getLayer(layer) && map.getLayoutProperty(layer, "visibility") !== "none");
  const producerHits = producerLayers.length ? map.queryRenderedFeatures(event.point, { layers: producerLayers }) : [];
  if (producerHits.length) {
    const feature = producerHits[0];
    if (feature.properties.cluster) {
      const source = map.getSource("producer-points");
      try {
        const zoom = await source.getClusterExpansionZoom(feature.properties.cluster_id);
        map.easeTo({ center: feature.geometry.coordinates, zoom, duration: transitionDuration(650) });
      } catch (error) {
        console.error(error);
        showToast("That producer cluster could not expand. Zoom in to keep exploring.");
      }
      return;
    }
    applyMapSelection({ areaFeatureIds: [], producerEntityId: feature.properties.carta_entity_id });
    await navigateSubject(feature.properties.carta_entity_id, { moveMap: false });
    return;
  }
  const layers = ["wine-region-labels", ...AOC_LAYERS]
    .filter((layer) => map.getLayer(layer) && map.getLayoutProperty(layer, "visibility") !== "none");
  if (state.igpLoaded && map.getLayoutProperty("igp-areas-fill") !== "none") layers.push("igp-areas-fill");
  const features = map.queryRenderedFeatures(event.point, { layers });
  if (!features.length) return;
  const unique = [...new Map(features.map((feature) => [feature.properties.source_denomination_id || feature.properties.source_feature_id, feature])).values()];
  const records = (await Promise.all(unique.map((feature) => searchRecordForFeature(feature)))).filter(Boolean);
  const primaryFeature = unique[0];
  // Overlap priority is editorial data, not a Jura-only map rule. It currently
  // makes Jurançon win over the broader Béarn layer and geographic Jura AOPs win
  // over overlapping category AOPs while retaining every record for explanation.
  const clickPriority = state.editorial?.map_click_priority || {};
  const preferredRecord = records
    .filter((record) => Number.isFinite(clickPriority[record.carta_entity_id]))
    .sort((a, b) => clickPriority[a.carta_entity_id] - clickPriority[b.carta_entity_id])[0];
  const primaryRecord = preferredRecord
    || records.find((record) => record.source_denomination_id === primaryFeature.properties.source_denomination_id)
    || records.find((record) => record.id === primaryFeature.properties.source_feature_id)
    || records[0];
  if (!primaryRecord) return;
  if (primaryRecord.carta_entity_id && state.subjects?.[primaryRecord.carta_entity_id]) {
    await navigateSubject(primaryRecord.carta_entity_id, { moveMap: true, overlaps: records });
  } else {
    await openMapRecord(primaryRecord, records, { focus: true });
  }
}

async function renderSources() {
  if (state.sourcesRendered) return;
  try {
    const response = await fetch(config.data.provenance);
    if (!response.ok) throw new Error("Provenance request failed");
    const provenance = await response.json();
    elements.sourcesContent.innerHTML = `
      <p class="sources-lede">The street map, official wine-area shapes, and Atlas's wine stories have different jobs. Keeping those jobs visible is how the Atlas stays honest.</p>
      <button class="about-link" type="button" data-open-about>What Atlas is for <span aria-hidden="true">→</span></button>
      <div class="source-cards">${provenance.datasets.map((dataset) => `
        <article class="source-card">
          <p class="source-class">${escapeHtml(dataset.authority_class.replaceAll("_", " "))}</p>
          <h3>${escapeHtml(dataset.dataset_title)}</h3>
          <p>${escapeHtml(dataset.geographic_meaning)}</p>
          <dl>
            <div><dt>Publisher</dt><dd>${escapeHtml(dataset.publisher)}</dd></div>
            <div><dt>Snapshot</dt><dd>${escapeHtml(dataset.source_release_date || "Runtime service")}</dd></div>
            <div><dt>License</dt><dd>${escapeHtml(dataset.license.id)}</dd></div>
          </dl>
          <a href="${escapeHtml(dataset.dataset_url)}" target="_blank" rel="noreferrer">View source <span aria-hidden="true">↗</span></a>
        </article>`).join("")}</div>
      <section class="semantic-note"><h3>Important distinctions</h3><ul>${provenance.semantic_distinctions.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul></section>
      <p class="source-counts">Current map reconciliation: ${provenance.inao_reconciliation.wine_features.toLocaleString()} wine features · ${provenance.inao_reconciliation.mapped_features} linked native subjects · ${provenance.inao_reconciliation.ambiguous_mappings} ambiguous.</p>`;
    state.sourcesRendered = true;
  } catch {
    elements.sourcesContent.innerHTML = "<p>The committed source notes could not be displayed. The map and its local learning data remain available.</p>";
  }
}

function entityIdFromHash() {
  const match = location.hash.match(/^#\/([^/]+)\/(.+)$/);
  if (!match) return null;
  return `${decodeURIComponent(match[1])}:${decodeURIComponent(match[2])}`;
}

async function bootstrapRoute() {
  await mapReady;
  try { await loadExperience(); } catch (error) { console.error(error); }
  renderTrail();
  const entityId = entityIdFromHash();
  if (entityId && state.subjects?.[entityId]) {
    const restore = history.state?.subjectId === entityId ? history.state : null;
    await enterFrance({ fit: !restore?.viewport, reveal: false });
    await navigateSubject(entityId, {
      moveMap: Boolean(!restore && state.subjects[entityId].map_target),
      historyMode: "replace",
      addTrail: !state.trail.some((step) => step.subjectId === entityId),
      restore,
    });
  }
}

map.on("load", () => {
  addWorldLayer();
  resolveMapReady();
  setStatus("World ready · select France to begin");
});
map.on("click", handleMapClick);
map.on("mousemove", (event) => {
  if (state.inspectMode) return;
  const layers = state.context === "world"
    ? ["france-country-fill"]
    : ["producer-clusters", "producer-points", "wine-region-labels", ...AOC_LAYERS].filter((layer) => map.getLayer(layer));
  map.getCanvas().style.cursor = layers.length && map.queryRenderedFeatures(event.point, { layers }).length ? "pointer" : "";
});
map.on("error", (event) => {
  console.error(event.error || event);
  setStatus("Some map context is unavailable · local wine data remains ready");
});

document.querySelector("[data-explore-france]").addEventListener("click", () => enterFrance());
document.querySelector("[data-world]").addEventListener("click", () => returnToWorld());
document.querySelector("[data-close-detail]").addEventListener("click", () => closeDetails());
elements.backButton.addEventListener("click", () => history.back());

elements.guidesButton.addEventListener("click", async () => {
  if (elements.discoveryPanel.hidden) {
    await enterFrance({ fit: state.context !== "france", reveal: false });
    await showDiscovery();
  } else hideDiscovery();
});
document.querySelector("[data-close-discovery]").addEventListener("click", hideDiscovery);

elements.rabbitButton.addEventListener("click", () => {
  const opening = elements.rabbitDrawer.getAttribute("aria-hidden") !== "false";
  elements.rabbitDrawer.setAttribute("aria-hidden", String(!opening));
  elements.rabbitDrawer.classList.toggle("is-open", opening);
  elements.rabbitButton.setAttribute("aria-expanded", String(opening));
  if (opening) hideDiscovery();
});
document.querySelector("[data-close-rabbit]").addEventListener("click", closeRabbit);
elements.rabbitTrail.addEventListener("click", (event) => {
  const button = event.target.closest("[data-restore-trail]");
  if (button) restoreTrailStep(Number(button.dataset.restoreTrail));
});

elements.layersButton.addEventListener("click", () => {
  const opening = elements.layerPanel.hidden;
  elements.layerPanel.hidden = !opening;
  elements.layersButton.setAttribute("aria-expanded", String(opening));
});
document.querySelector("[data-close-layers]").addEventListener("click", () => {
  elements.layerPanel.hidden = true;
  elements.layersButton.setAttribute("aria-expanded", "false");
});

elements.aocToggle.addEventListener("change", async () => {
  await enterFrance({ fit: state.context !== "france", reveal: false });
  setLayerVisibility(["aoc-areas-fill", "aoc-areas-line", "aoc-complements-fill", "aoc-labels", "subject-areas-fill", "subject-areas-line"], elements.aocToggle.checked);
});
elements.igpToggle.addEventListener("change", async () => {
  if (elements.igpToggle.checked) await ensureIgpData();
  setLayerVisibility(["igp-areas-fill"], elements.igpToggle.checked);
});
elements.regionsToggle.addEventListener("change", async () => {
  await enterFrance({ fit: state.context !== "france", reveal: false });
  setLayerVisibility(REGION_LAYERS, elements.regionsToggle.checked);
});
elements.producersToggle.addEventListener("change", async () => {
  await enterFrance({ fit: state.context !== "france", reveal: false });
  setLayerVisibility([...PRODUCER_LAYERS, "producer-selection", "subject-producer-halos", "subject-producer-labels"], elements.producersToggle.checked);
});

elements.inspectButton.addEventListener("click", async () => {
  await enterFrance({ fit: state.context !== "france", reveal: false });
  setInspectMode(!state.inspectMode);
});

elements.searchInput.addEventListener("input", renderSearch);
elements.searchInput.addEventListener("keydown", (event) => {
  if (event.key === "ArrowDown") { event.preventDefault(); updateActiveSearch(state.activeSearchIndex + 1); }
  if (event.key === "ArrowUp") { event.preventDefault(); updateActiveSearch(state.activeSearchIndex - 1); }
  if (event.key === "Escape") closeSearch();
});
elements.searchForm.addEventListener("submit", (event) => {
  event.preventDefault();
  selectSearchResult(state.activeSearchIndex >= 0 ? state.activeSearchIndex : 0);
});
elements.searchResults.addEventListener("click", (event) => {
  const option = event.target.closest("[data-result-index]");
  if (option) selectSearchResult(Number(option.dataset.resultIndex));
});

elements.discoveryContent.addEventListener("click", (event) => {
  const go = event.target.closest("[data-go-to-subject]");
  if (go) navigateSubject(go.dataset.goToSubject, { moveMap: true });
  const entry = event.target.closest("[data-entry-subject]");
  if (entry) {
    const subject = state.subjects[entry.dataset.entrySubject];
    const moveMap = ["place", "appellation"].includes(subject.kind) && Boolean(subject.map_target);
    navigateSubject(subject.entity_id, { moveMap });
  }
});

elements.detailContent.addEventListener("click", async (event) => {
  const termTrigger = event.target.closest("[data-term-id]");
  if (termTrigger) {
    const wrapper = termTrigger.closest(".inline-term");
    const opening = !wrapper.classList.contains("is-open");
    elements.detailContent.querySelectorAll(".inline-term.is-open").forEach((item) => item.classList.remove("is-open"));
    elements.detailContent.querySelectorAll("[data-term-id][aria-expanded='true']").forEach((item) => item.setAttribute("aria-expanded", "false"));
    wrapper.classList.toggle("is-open", opening);
    termTrigger.setAttribute("aria-expanded", String(opening));
    return;
  }
  const pillar = event.target.closest("[data-region-pillar-target]");
  if (pillar) {
    activateRegionalPillar(pillar.dataset.regionPillarTarget);
    return;
  }
  const pillarSummary = event.target.closest("[data-region-pillar-summary]");
  if (pillarSummary) {
    const details = pillarSummary.closest(".jura-pillar");
    if (!details.open && window.matchMedia("(max-width: 720px)").matches) {
      elements.detailContent.querySelectorAll(".jura-pillar[open]").forEach((item) => { item.open = false; });
    }
    activateRegionalPillar(pillarSummary.dataset.regionPillarSummary, { manageDetails: false, scroll: false });
    return;
  }
  const mapReaction = event.target.closest("[data-region-map-reaction]");
  if (mapReaction) {
    activateRegionalPillar(mapReaction.dataset.regionMapReaction, { manageDetails: false, scroll: false });
    return;
  }
  const explore = event.target.closest("[data-explore-subject]");
  if (explore) {
    await navigateSubject(explore.dataset.exploreSubject, { moveMap: false });
    return;
  }
  const go = event.target.closest("[data-go-to-subject]");
  if (go) {
    await navigateSubject(go.dataset.goToSubject, { moveMap: true });
    return;
  }
  const current = event.target.closest("[data-go-to-current]");
  if (current && state.activeSubjectId) {
    const subject = state.subjects[state.activeSubjectId];
    await moveToMapTarget(subject);
    recordTrail(subject, { moved: true });
    history.replaceState(historyStateFor(subject, history.state?.fromSubjectId || null), "", `${location.pathname}${location.search}${subject.route}`);
    const guide = state.atlasGuides[subject.entity_id] || null;
    renderPanelMarkup(subjectCardMarkup(subject, guide, state.activeOverlapRecords));
    applySubjectMapReaction(subject);
    updateBackButton();
    return;
  }
  const restore = event.target.closest("[data-restore-trail]");
  if (restore) {
    await restoreTrailStep(Number(restore.dataset.restoreTrail));
    return;
  }
  const recordButton = event.target.closest("[data-go-to-record]");
  if (recordButton) {
    const records = await loadSearchIndex();
    const record = records.find((item) => item.id === recordButton.dataset.goToRecord);
    if (record) await openMapRecord(record, state.activeOverlapRecords, { focus: true });
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "/" && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) {
    event.preventDefault();
    elements.searchInput.focus();
  }
  if (event.key === "Escape") {
    if (state.inspectMode) setInspectMode(false);
    else if (elements.rabbitDrawer.classList.contains("is-open")) closeRabbit();
    else if (!elements.discoveryPanel.hidden) hideDiscovery();
    else if (elements.detailPanel.classList.contains("is-open")) closeDetails();
  }
});
document.addEventListener("click", (event) => { if (!elements.searchForm.contains(event.target)) closeSearch(); });

document.querySelector("[data-sources-button]").addEventListener("click", async () => {
  await renderSources();
  elements.sourcesDialog.showModal();
});
document.querySelector("[data-close-sources]").addEventListener("click", () => elements.sourcesDialog.close());
elements.sourcesContent.addEventListener("click", (event) => {
  if (!event.target.closest("[data-open-about]")) return;
  elements.sourcesDialog.close();
  elements.aboutDialog.showModal();
});
document.querySelector("[data-close-about]").addEventListener("click", () => elements.aboutDialog.close());
document.querySelector("[data-open-sources-from-about]").addEventListener("click", async () => {
  elements.aboutDialog.close();
  await renderSources();
  elements.sourcesDialog.showModal();
});
elements.aboutDialog.addEventListener("click", (event) => { if (event.target === elements.aboutDialog) elements.aboutDialog.close(); });
elements.sourcesDialog.addEventListener("click", (event) => { if (event.target === elements.sourcesDialog) elements.sourcesDialog.close(); });

window.addEventListener("popstate", async (event) => {
  const entityId = entityIdFromHash();
  if (entityId && state.subjects?.[entityId]) {
    await navigateSubject(entityId, {
      moveMap: false,
      historyMode: "none",
      addTrail: false,
      restore: event.state?.subjectId === entityId ? event.state : null,
    });
  } else returnToWorld({ updateHistory: false });
});
window.addEventListener("resize", () => map.resize());

bootstrapRoute();

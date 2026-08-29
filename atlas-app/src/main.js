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
  inspectButton: document.querySelector("[data-inspect-button]"),
  sourcesDialog: document.querySelector("[data-sources-dialog]"),
  sourcesContent: document.querySelector("[data-sources-content]"),
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
  entryPoints: null,
  producerFeatures: null,
  searchMatches: [],
  activeSearchIndex: -1,
  activeSubjectId: null,
  activeOverlapRecords: [],
  activeMapSelection: null,
  geographicSubjectId: null,
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

  map.addLayer({
    id: "aoc-areas-fill",
    type: "fill",
    source: "aoc-areas",
    minzoom: config.semanticZoom.appellationFillMin,
    filter: ["!=", ["get", "feature_type"], "geographical_complement"],
    layout: { visibility: elements.aocToggle.checked ? "visible" : "none" },
    paint: {
      "fill-color": ["case", ["==", ["get", "governance_status"], "governed"], "#7f2f3f", "#b48468"],
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
    paint: { "text-color": "#304e42", "text-halo-color": "#fffdf8", "text-halo-width": 2 },
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
      "circle-color": "#304e42",
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
      "circle-color": "#304e42",
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
    paint: { "text-color": "#213b32", "text-halo-color": "#fffdf8", "text-halo-width": 1.7 },
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
  map.flyTo({ ...WORLD_VIEW, duration: transitionDuration(1000), essential: true });
  setStatus("World ready · select France to begin");
  if (updateHistory) history.pushState({ subjectId: null }, "", `${location.pathname}${location.search}`);
}

async function loadExperience() {
  if (state.subjects && state.entryPoints && state.producerFeatures && state.atlasGuides) return;
  const [subjectResponse, entryResponse, producerResponse, guideResponse] = await Promise.all([
    fetch(config.data.atlasSubjects),
    fetch(config.data.entryPoints),
    fetch(config.data.producerPoints),
    fetch(config.data.atlasGuides),
  ]);
  for (const response of [subjectResponse, entryResponse, producerResponse, guideResponse]) {
    if (!response.ok) throw new Error(`Atlas learning data request failed (${response.status})`);
  }
  state.subjects = (await subjectResponse.json()).subjects;
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

function connectionNote(connection) {
  const labels = {
    GENETICALLY_CLOSE_TO: "Genetically close — not a parentage claim",
    TRADITIONAL_IN: "A place where this matters",
    USED_BY: connection.direction === "outbound" ? "A producer working with it" : "A grape in the picture",
    MADE_FROM: connection.direction === "outbound" ? "Made with" : "A wine made from this",
    MADE_BY: connection.direction === "outbound" ? "Made by" : "A wine from this producer",
    USES_PRACTICE: connection.direction === "outbound" ? "A cellar choice" : "A wine that makes it concrete",
    CLASSIFIED_AS: "Wine-area connection",
    LOCATED_IN: "Based here",
    CELLAR_IN: "Production base",
    WITHIN: "Part of this place",
    PROFILE_COMPONENT: "Wine area to explore",
    EXPLORE: "A useful next turn",
  };
  return labels[connection.predicate] || "Connected in CARTA";
}

function exploreVerb(kind) {
  return kind === "producer" ? "Meet" : "Explore";
}

function mapVerb(connection) {
  if (connection.target_kind === "producer") return "Show on map";
  return `Go to ${connection.target_name.replace(/ AOP$/, "")}`;
}

function connectionMarkup(subject) {
  if (!subject.connections.length) return "";
  const priority = { grape: 0, producer: 1, appellation: 2, place: 3, wine: 4, practice: 5 };
  const connections = [...subject.connections]
    .sort((a, b) => {
      if (a.predicate === "GENETICALLY_CLOSE_TO" && b.predicate !== "GENETICALLY_CLOSE_TO") return -1;
      if (b.predicate === "GENETICALLY_CLOSE_TO" && a.predicate !== "GENETICALLY_CLOSE_TO") return 1;
      return (priority[a.target_kind] ?? 9) - (priority[b.target_kind] ?? 9) || a.target_name.localeCompare(b.target_name);
    })
    .slice(0, 18);
  return `
    <section class="detail-section connection-section">
      <h3>Where next?</h3>
      <div class="connection-list">${connections.map((connection) => `
        <article class="connection-card ${connection.predicate === "GENETICALLY_CLOSE_TO" ? "connection-card--surprise" : ""}">
          ${connection.predicate === "GENETICALLY_CLOSE_TO" ? '<p class="connection-surprise">Unexpected turn</p>' : ""}
          <button class="connection-subject" type="button" data-explore-subject="${escapeHtml(connection.target_id)}">
            <span>${escapeHtml(connection.target_name)}</span>
            <small>${escapeHtml(connectionNote(connection))}</small>
          </button>
          <div class="connection-actions">
            <button type="button" data-explore-subject="${escapeHtml(connection.target_id)}">${exploreVerb(connection.target_kind)}</button>
            ${connection.has_map_target ? `<button class="connection-go" type="button" data-go-to-subject="${escapeHtml(connection.target_id)}">${escapeHtml(mapVerb(connection))}</button>` : ""}
          </div>
        </article>`).join("")}</div>
    </section>`;
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

function returnToSavagninMarkup() {
  const index = [...state.trail].map((step) => step.subjectId).lastIndexOf("grape:savagnin");
  if (index < 0 || state.activeSubjectId === "grape:savagnin") return "";
  const center = map.loaded() ? map.getCenter() : null;
  const leftJura = state.geographicSubjectId === "appellation:jurancon" || (center && center.lng < 2.5);
  if (!leftJura) return "";
  return `<button class="return-context" type="button" data-restore-trail="${index}">← Back to Savagnin in Jura</button>`;
}

function fallbackSubjectLede(subject) {
  const copy = {
    practice: "A cellar choice best understood through the wines and producers that make it concrete.",
    wine: "A bottle-level way into its producer, grapes, place, and cellar choices.",
    place: "A local place best understood through the producers and wine areas connected to it.",
    person: "A person whose connections help explain part of this wine world.",
  };
  return copy[subject.kind] || "A useful way into the places, people, bottles, and relationships around it.";
}

function subjectCardMarkup(subject, guide = null, overlaps = []) {
  const lead = subject.claims.find((claim) => claim.claim_id === subject.lead_claim_id) || subject.claims[0];
  const quantitativeClaimIds = new Set((guide?.quantities || []).map((item) => item.claim_id));
  const claims = subject.claims
    .filter((claim) => claim !== lead && !quantitativeClaimIds.has(claim.claim_id))
    .slice(0, 5);
  const placement = producerPlacement(subject);
  const special = subject.entity_id === "grape:savagnin"
    ? '<p class="rabbit-whisper">One grape. Several cellar paths. A very good place to get lost.</p>'
    : "";
  const currentMapAction = subject.map_target
    ? `<button class="secondary-action" type="button" data-go-to-current>${subject.kind === "producer" ? "Show this domaine on the map" : `Go to ${escapeHtml(subject.display_name.replace(/ AOP$/, ""))}`}</button>`
    : "";
  const claimSections = claims.map((claim) => `
    <section class="detail-section claim-section ${claim.status === "contested" ? "claim-section--note" : ""}">
      <h3>${escapeHtml(claim.status === "contested" ? "A source note" : claimLabel(claim))}</h3>
      ${claim.subject_ref !== subject.entity_id ? `<p class="claim-subject">About ${escapeHtml(claim.subject_name)}</p>` : ""}
      <p>${escapeHtml(claim.statement)}</p>
    </section>`).join("");
  return `
    ${returnToSavagninMarkup()}
    <p class="detail-eyebrow">${escapeHtml(subject.kind_label)}</p>
    <h2>${escapeHtml(subject.display_name)}</h2>
    ${placement ? `<p class="subject-place">${escapeHtml(placement)}</p>` : ""}
    ${special}
    ${lead ? `<p class="guide-lede">${escapeHtml(lead.statement)}</p>` : `<p class="guide-lede">${escapeHtml(fallbackSubjectLede(subject))}</p>`}
    ${currentMapAction ? `<div class="subject-actions">${currentMapAction}</div>` : ""}
    ${guideFactsMarkup(guide)}
    ${claimSections}
    ${overlapMarkup(overlaps)}
    ${connectionMarkup(subject)}
    ${sourcesMarkup(subject.sources)}
    <details class="detail-disclosure technical-disclosure"><summary>Technical details</summary><dl>
      <div><dt>CARTA identity</dt><dd><code>${escapeHtml(subject.entity_id)}</code></dd></div>
      <div><dt>Route</dt><dd><code>${escapeHtml(subject.route)}</code></dd></div>
      ${subject.location ? `<div><dt>Map precision</dt><dd>${escapeHtml(subject.location.precision)}</dd></div>` : ""}
    </dl></details>`;
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
    <p class="guide-lede">The map has reliable official coverage here. A fuller story can grow later; for now, use the shape to orient yourself and compare the wine areas around it.</p>
    <button class="secondary-action" type="button" data-go-to-record="${escapeHtml(record.id)}">Go to this area</button>
    ${overlapMarkup(overlaps)}
    <details class="detail-disclosure"><summary>What this shape means</summary><p>${escapeHtml(sourceMeaning)}</p></details>
    <details class="detail-disclosure technical-disclosure"><summary>Technical details</summary><dl>
      <div><dt>Representation</dt><dd>${escapeHtml(record.representation_label || record.representation_type || "Sourced map feature")}</dd></div>
      <div><dt>Map source</dt><dd>${escapeHtml(isRegion ? "CARTA derivation from mapped INAO child areas" : "INAO SIQO geographical areas")}</dd></div>
      ${record.carta_entity_id ? `<div><dt>CARTA identity</dt><dd><code>${escapeHtml(record.carta_entity_id)}</code></dd></div>` : ""}
    </dl></details>`;
}

function openPanel(markup) {
  elements.detailPanel.setAttribute("aria-hidden", "false");
  elements.detailPanel.classList.add("is-open");
  elements.detailContent.innerHTML = markup;
  elements.detailContent.scrollTop = 0;
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

function historyStateFor(subject) {
  return {
    subjectId: subject.entity_id,
    viewport: captureViewport(),
    selection: state.activeMapSelection,
    geographicSubjectId: state.geographicSubjectId,
    panelOpen: true,
  };
}

function setHistory(subject, mode) {
  if (mode === "none") return;
  const method = mode === "replace" ? "replaceState" : "pushState";
  history[method](historyStateFor(subject), "", `${location.pathname}${location.search}${subject.route}`);
}

async function moveToMapTarget(subject, { selection = null } = {}) {
  const target = subject.map_target;
  if (!target) return false;
  await enterFrance({ fit: false, reveal: false });
  state.geographicSubjectId = subject.entity_id;
  if (target.kind === "bounds") {
    const areaFeatureIds = target.map_feature_ids.filter((id) => id.startsWith("inao-"));
    applyMapSelection(selection || { areaFeatureIds, producerEntityId: null });
    map.fitBounds(target.bounds, {
      padding: panelPadding(),
      maxZoom: target.max_zoom,
      duration: transitionDuration(900),
      essential: true,
    });
  } else if (target.kind === "point") {
    applyMapSelection(selection || { areaFeatureIds: [], producerEntityId: subject.entity_id });
    map.flyTo({
      center: target.center,
      zoom: target.zoom,
      padding: panelPadding(),
      duration: transitionDuration(900),
      essential: true,
    });
  }
  if (subject.entity_id === "appellation:jurancon") {
    showToast("You've wandered from Jura to the western Pyrenees.");
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
    if (addTrail) recordTrail(subject, { moved });
    else renderTrail();
    setHistory(subject, historyMode);
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
  if (step.subjectId === "grape:savagnin") showToast("Back to Savagnin, with Jura exactly where you left it.");
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
    showToast("Starting points could not load. Search and the map remain available.");
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
  const jura = state.subjects["place:jura"];
  const juraAops = new Set(jura.connections.filter((item) => item.target_kind === "appellation").map((item) => item.target_id));
  const inJura = records.some((record) => juraAops.has(record.carta_entity_id));
  const grapes = inJura ? jura.connections.filter((item) => item.target_kind === "grape").slice(0, 5) : [];
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
    <h2>${inJura ? "A point in Jura's overlapping wine world" : "A point on the wine map"}</h2>
    <p class="guide-lede">${inJura ? "Several wine rules can occupy the same ground while describing different origins, categories, and methods." : "Here is what the visible sourced geography can say about the point you chose."}</p>
    <section class="detail-section"><h3>Wine areas covering this point</h3>${areasMarkup}</section>
    ${grapesMarkup}
    ${producersMarkup}
    ${inJura ? '<section class="detail-section inspection-why"><h3>Why this is interesting</h3><p>Jura makes overlap unusually legible: a geographic still-wine origin can share ground with sparkling or mistelle rules without becoming the same kind of wine.</p></section>' : ""}
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
  const primaryRecord = records.find((record) => record.source_denomination_id === primaryFeature.properties.source_denomination_id)
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
      <p class="sources-lede">The street map, official wine-area shapes, and CARTA's wine stories have different jobs. Keeping those jobs visible is how the Atlas stays honest.</p>
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
  setLayerVisibility(["aoc-areas-fill", "aoc-areas-line", "aoc-complements-fill", "aoc-labels"], elements.aocToggle.checked);
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
  setLayerVisibility([...PRODUCER_LAYERS, "producer-selection"], elements.producersToggle.checked);
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
    history.replaceState(historyStateFor(subject), "", `${location.pathname}${location.search}${subject.route}`);
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

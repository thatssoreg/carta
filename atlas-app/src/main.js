import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import config from "./atlas-config.json";
import "./styles.css";

const WORLD_VIEW = { center: [5, 34], zoom: 1.65, bearing: 0, pitch: 0 };
const FRANCE_PHONE_VIEW = { center: [2.15, 46.5], zoom: 4.45, bearing: 0, pitch: 0 };
const FRANCE_BOUNDS = config.countries.france.bounds;
const AOC_LAYERS = ["aoc-complements-fill", "aoc-areas-fill"];
const INTERACTIVE_LAYERS = ["wine-region-labels", ...AOC_LAYERS];

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
  detailPanel: document.querySelector("[data-detail-panel]"),
  detailContent: document.querySelector("[data-detail-content]"),
  sourcesDialog: document.querySelector("[data-sources-dialog]"),
  sourcesContent: document.querySelector("[data-sources-content]"),
  toast: document.querySelector("[data-toast]"),
};

const state = {
  context: "world",
  franceLoaded: false,
  igpLoaded: false,
  searchIndex: null,
  atlasGuides: null,
  searchMatches: [],
  activeSearchIndex: -1,
  sourcesRendered: false,
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
map.addControl(
  new maplibregl.AttributionControl({ compact: true }),
  "bottom-right",
);

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
  showToast.timer = window.setTimeout(() => { elements.toast.hidden = true; }, 5000);
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
}

async function ensureFranceData() {
  await mapReady;
  if (state.franceLoaded) return;
  setStatus("Loading sourced France wine geography…", true);
  addFranceLayers();
  state.franceLoaded = true;
  setStatus("France · 5 region guides · 32 governed appellation areas");
}

async function ensureIgpData() {
  await ensureFranceData();
  if (state.igpLoaded) return;
  setStatus("Loading 165 IGP areas…", true);
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
  setStatus("France · AOC + IGP regulatory area layers");
}

function panelPadding() {
  return window.matchMedia("(max-width: 720px)").matches
    ? { top: 55, right: 24, bottom: elements.detailPanel.getAttribute("aria-hidden") === "false" ? 260 : 45, left: 24 }
    : { top: 90, right: elements.detailPanel.getAttribute("aria-hidden") === "false" ? 500 : 60, bottom: 60, left: 60 };
}

async function enterFrance({ fit = true } = {}) {
  await ensureFranceData();
  state.context = "france";
  elements.intro.hidden = true;
  elements.context.textContent = "France";
  if (fit && window.matchMedia("(max-width: 720px)").matches) {
    map.flyTo({ ...FRANCE_PHONE_VIEW, duration: 1300, essential: true });
  } else if (fit) {
    map.fitBounds(FRANCE_BOUNDS, { padding: panelPadding(), maxZoom: config.countries.france.maxZoom, duration: 1300, essential: true });
  }
}

function returnToWorld() {
  state.context = "world";
  elements.intro.hidden = false;
  elements.context.textContent = "Orientation";
  closeDetails();
  closeSearch();
  map.flyTo({ ...WORLD_VIEW, duration: 1200, essential: true });
  setStatus("World ready · select France to enter the wine atlas");
}

function normalizeBounds(value) {
  if (Array.isArray(value)) return value;
  try { return JSON.parse(value); } catch { return null; }
}

function humanReferenceUrl(path) {
  return path ? `${config.humanReference.repositoryBaseUrl}${path}` : null;
}

function featureRecord(feature) {
  return feature?.properties ?? feature ?? {};
}

function formatQuantity(quantity) {
  const value = Number(quantity.value).toLocaleString(undefined, { maximumFractionDigits: 2 });
  if (quantity.unit === "percent") return `${value}%`;
  if (quantity.unit === "ha") return `${value} ha`;
  if (quantity.unit === "km") return `${value} km`;
  return value;
}

function measureLabel(measure) {
  return {
    grape_share: "Grape picture",
    wine_color_share: "Wine colors",
    production_tier_share: "Production by appellation tier",
  }[measure] || "Measured picture";
}

function sectionLabel(section) {
  return {
    why_it_matters: "Why it matters",
    wine_picture: "The wine picture",
    physical_place: "The physical place",
    hierarchy: "How to read the hierarchy",
    map_meaning: "What the map means",
  }[section] || "In context";
}

function guideMarkup(record, guide, overlaps, sourceMeaning) {
  const lead = guide.sections.find((item) => item.section === "orientation");
  const narrative = [...guide.sections, ...guide.quantities.filter((item) => item.section !== "quick_fact")]
    .filter((item) => !["orientation", "quick_fact"].includes(item.section))
    .sort((a, b) => a.order - b.order || a.claim_id.localeCompare(b.claim_id))
    .map((item) => `
      <section class="detail-section guide-section">
        <h3>${escapeHtml(item.label || sectionLabel(item.section))}</h3>
        <p>${escapeHtml(item.statement)}</p>
      </section>`).join("");
  const measured = guide.quantities.filter((item) => item.quantity.unit !== "percent");
  const measuredMarkup = measured.length ? `
    <section class="detail-section measured-section">
      <h3>At a glance</h3>
      <div class="fact-grid">${measured.slice(0, 6).map((item) => `
        <article class="fact-card">
          <strong>${escapeHtml(formatQuantity(item.quantity))}</strong>
          <span>${escapeHtml(item.label || item.quantity.dimension_name || item.quantity.dimension_label || item.subject_name)}</span>
          <small>${escapeHtml(item.observed_at?.slice(0, 4) || "Dated source")}</small>
        </article>`).join("")}</div>
    </section>` : "";
  const shares = [...new Set(guide.quantities
    .filter((item) => item.quantity.unit === "percent")
    .map((item) => item.quantity.measure))];
  const sharesMarkup = shares.map((measure) => {
    const items = guide.quantities.filter((item) => item.quantity.measure === measure);
    const context = items[0]?.quantity.scope;
    return `
      <section class="detail-section share-section">
        <h3>${escapeHtml(measureLabel(measure))}</h3>
        <div class="share-bars">${items.map((item) => `
          <div class="share-row">
            <div><span>${escapeHtml(item.label || item.quantity.dimension_name || item.quantity.dimension_label)}</span><strong>${escapeHtml(formatQuantity(item.quantity))}</strong></div>
            <div class="share-track" aria-hidden="true"><i style="width:${Math.max(2, Math.min(100, item.quantity.value))}%"></i></div>
          </div>`).join("")}</div>
        <p class="measure-note">${escapeHtml(context)} · ${escapeHtml(items[0]?.observed_at?.slice(0, 4) || "dated source")}</p>
      </section>`;
  }).join("");
  const exploreMarkup = guide.explore.length ? `
    <section class="detail-section explore-section">
      <h3>Keep exploring</h3>
      <div class="explore-links">${guide.explore.slice(0, 8).map((item) => `
        <a href="${escapeHtml(humanReferenceUrl(item.human_reference_path))}" target="_blank" rel="noreferrer">
          <span>${escapeHtml(item.label)}</span><span aria-hidden="true">↗</span>
        </a>`).join("")}</div>
    </section>` : "";
  const sourceMarkup = guide.sources.filter((source) => source.url).map((source) => `
    <li><a href="${escapeHtml(source.url)}" target="_blank" rel="noreferrer">${escapeHtml(source.title)}</a><small>${escapeHtml(source.publisher || "Source")}${source.publication_date ? ` · ${escapeHtml(source.publication_date.slice(0, 4))}` : ""}</small></li>`).join("");
  const overlapItems = overlaps
    .filter((item) => item.source_denomination_id !== record.source_denomination_id)
    .slice(0, 8)
    .map((item) => `<li><span>${escapeHtml(item.name)}</span><small>${escapeHtml(item.designation || "AOC")}</small></li>`)
    .join("");
  const reference = humanReferenceUrl(guide.human_reference_path || record.human_reference_path);
  const aliasNote = guide.guide_entity_id !== record.carta_entity_id
    ? `<p class="guide-context">This mapped area opens the broader ${escapeHtml(guide.title)} guide.</p>`
    : "";

  return `
    <p class="detail-eyebrow">${record.feature_type === "wine_region_orientation" || record.result_type === "wine_region" ? "Region guide" : `${escapeHtml(record.designation || "Wine")} place guide`}</p>
    <h2>${escapeHtml(record.name)}</h2>
    ${aliasNote}
    <p class="guide-lede">${escapeHtml(lead?.statement || guide.sections[0]?.statement || "A governed path into this wine place.")}</p>
    <div class="detail-badges"><span class="badge badge--governed">Governed CARTA guide</span><span class="badge">${escapeHtml(guide.maturity)} reference</span></div>
    ${measuredMarkup}
    ${sharesMarkup}
    ${narrative}
    ${exploreMarkup}
    ${overlapItems ? `<section class="detail-section overlap-section"><h3>Wine areas that overlap here</h3><p>Wine rules can cover the same point for different origins, categories, or geographic levels. Overlap is context—not an error.</p><ul class="overlap-list">${overlapItems}</ul></section>` : ""}
    <details class="detail-disclosure"><summary>What this map shape means</summary><p>${escapeHtml(sourceMeaning)}</p></details>
    <details class="detail-disclosure"><summary>Sources &amp; notes <span>${guide.sources.length}</span></summary><ul class="guide-sources">${sourceMarkup}</ul></details>
    <details class="detail-disclosure technical-disclosure"><summary>Technical details</summary><dl>
      <div><dt>Representation</dt><dd>${escapeHtml(record.representation_label || record.representation_type || "Sourced map feature")}</dd></div>
      ${record.source_release_date ? `<div><dt>Map snapshot</dt><dd>${escapeHtml(record.source_release_date)}</dd></div>` : ""}
      ${record.carta_entity_id ? `<div><dt>CARTA identity</dt><dd><code>${escapeHtml(record.carta_entity_id)}</code></dd></div>` : ""}
    </dl></details>
    ${reference ? `<a class="reference-link" href="${escapeHtml(reference)}" target="_blank" rel="noreferrer">Read the full Human Reference <span aria-hidden="true">↗</span></a>` : ""}
  `;
}

function detailMarkup(record, overlaps = [], guide = null) {
  const governed = record.governance_status === "governed";
  const isRegion = record.feature_type === "wine_region_orientation" || record.result_type === "wine_region";
  const designation = isRegion ? "Region orientation" : `${record.designation || "Wine"} ${record.feature_type === "geographical_complement" ? "geographic denomination" : "area"}`;
  const sourceMeaning = isRegion
    ? "This point is derived from mapped child-appellation areas for orientation. It is not a statutory wine-region boundary."
    : "This shape is INAO’s cartographic representation of the regulatory geographical area. It is not a map of approved parcels or actual planted vineyard land.";
  if (guide) return guideMarkup(record, guide, overlaps, sourceMeaning);
  const reference = humanReferenceUrl(record.human_reference_path);
  const overlapItems = overlaps
    .filter((item) => item.source_denomination_id !== record.source_denomination_id)
    .slice(0, 8)
    .map((item) => `<li><span>${escapeHtml(item.name)}</span><small>${escapeHtml(item.designation || "AOC")}</small></li>`)
    .join("");

  return `
    <p class="detail-eyebrow">${escapeHtml(designation)} · map coverage</p>
    <h2>${escapeHtml(record.name)}</h2>
    <div class="detail-badges">
      <span class="badge ${governed ? "badge--governed" : ""}">${governed ? "Governed map identity" : "Official map coverage"}</span>
    </div>
    <section class="detail-section"><h3>What you can learn here</h3><p>This release has reliable map coverage for this area, but not yet a full learner guide. Use the shape to orient yourself and compare nearby wine areas.</p></section>
    ${overlapItems ? `<section class="detail-section"><h3>Wine areas that overlap here</h3><p>Different wine rules can cover the same point. Overlap is context—not an error.</p><ul class="overlap-list">${overlapItems}</ul></section>` : ""}
    <details class="detail-disclosure"><summary>Map meaning &amp; technical details</summary><p>${escapeHtml(sourceMeaning)}</p>
      <dl>
        <div><dt>Representation</dt><dd>${escapeHtml(record.representation_label || record.representation_type || "Sourced map feature")}</dd></div>
        <div><dt>Source</dt><dd>${escapeHtml(isRegion ? "CARTA derivation from mapped INAO child areas" : "INAO SIQO geographical areas")}</dd></div>
        ${record.carta_entity_id ? `<div><dt>CARTA identity</dt><dd><code>${escapeHtml(record.carta_entity_id)}</code></dd></div>` : ""}
      </dl>
    </details>
    ${reference ? `<a class="reference-link" href="${escapeHtml(reference)}" target="_blank" rel="noreferrer">Read the Human Reference <span aria-hidden="true">↗</span></a>` : `<p class="reference-empty">A full CARTA guide has not been published for this area yet.</p>`}
  `;
}

async function loadAtlasGuides() {
  if (!state.atlasGuides) {
    const response = await fetch(config.data.atlasGuides);
    if (!response.ok) throw new Error(`Atlas guides request failed (${response.status})`);
    state.atlasGuides = (await response.json()).guides;
  }
  return state.atlasGuides;
}

async function openDetails(record, overlaps = []) {
  const feature = featureRecord(record);
  const overlapRecords = overlaps.map(featureRecord);
  elements.detailPanel.setAttribute("aria-hidden", "false");
  elements.detailPanel.classList.add("is-open");
  elements.detailContent.innerHTML = `<p class="detail-loading">Opening ${escapeHtml(feature.name)}…</p>`;
  elements.detailContent.scrollTop = 0;
  map.easeTo({ padding: panelPadding(), duration: 350 });
  try {
    const guides = await loadAtlasGuides();
    elements.detailContent.innerHTML = detailMarkup(feature, overlapRecords, guides[feature.carta_entity_id] || null);
    elements.detailContent.scrollTop = 0;
  } catch {
    elements.detailContent.innerHTML = detailMarkup(feature, overlapRecords);
    elements.detailContent.scrollTop = 0;
    showToast("The learning guide could not load; official map context remains available.");
  }
}

function closeDetails() {
  elements.detailPanel.setAttribute("aria-hidden", "true");
  elements.detailPanel.classList.remove("is-open");
  if (map.loaded()) map.easeTo({ padding: { top: 0, right: 0, bottom: 0, left: 0 }, duration: 250 });
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

async function renderSearch() {
  const query = elements.searchInput.value.trim().toLocaleLowerCase();
  if (query.length < 2) { closeSearch(); return; }
  try {
    const records = await loadSearchIndex();
    state.searchMatches = records
      .filter((record) => record.name.toLocaleLowerCase().includes(query))
      .sort((a, b) => searchScore(a, query) - searchScore(b, query) || a.name.localeCompare(b.name))
      .slice(0, 10);
    state.activeSearchIndex = state.searchMatches.length ? 0 : -1;
    elements.searchResults.innerHTML = state.searchMatches.length
      ? state.searchMatches.map((record, index) => `
          <button id="search-option-${index}" type="button" role="option" aria-selected="${index === 0}" data-result-index="${index}">
            <span>${escapeHtml(record.name)}</span>
            <small>${record.result_type === "wine_region" ? "Region guide" : `${escapeHtml(record.designation)} · ${record.governance_status === "governed" ? "Guide + official map" : "Official map"}`}</small>
          </button>`).join("")
      : `<p class="search-empty">No France wine geography matches “${escapeHtml(elements.searchInput.value.trim())}”.</p>`;
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

async function selectSearchResult(index) {
  const record = state.searchMatches[index];
  if (!record) return;
  closeSearch();
  elements.searchInput.value = record.name;
  await enterFrance({ fit: false });
  openDetails(record);
  const bounds = normalizeBounds(record.bounds);
  if (bounds) map.fitBounds(bounds, { padding: panelPadding(), maxZoom: record.result_type === "wine_region" ? 7.4 : 10.4, duration: 900, essential: true });
}

function updateActiveSearch(nextIndex) {
  if (!state.searchMatches.length) return;
  state.activeSearchIndex = (nextIndex + state.searchMatches.length) % state.searchMatches.length;
  elements.searchResults.querySelectorAll("[role='option']").forEach((option, index) => option.setAttribute("aria-selected", String(index === state.activeSearchIndex)));
  const active = elements.searchResults.querySelector(`[data-result-index="${state.activeSearchIndex}"]`);
  elements.searchInput.setAttribute("aria-activedescendant", active.id);
  active.scrollIntoView({ block: "nearest" });
}

async function renderSources() {
  if (state.sourcesRendered) return;
  try {
    const response = await fetch(config.data.provenance);
    if (!response.ok) throw new Error("Provenance request failed");
    const provenance = await response.json();
    elements.sourcesContent.innerHTML = `
      <p class="sources-lede">CARTA separates ordinary basemap context, sourced regulatory geography, and governed wine identity. Display does not silently promote external data into the knowledge model.</p>
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
      <p class="source-counts">Current reconciliation: ${provenance.inao_reconciliation.wine_features.toLocaleString()} wine features · ${provenance.inao_reconciliation.mapped_features} accepted CARTA mappings · ${provenance.inao_reconciliation.ambiguous_mappings} ambiguous.</p>
    `;
    state.sourcesRendered = true;
  } catch {
    elements.sourcesContent.innerHTML = "<p>Committed provenance could not be displayed. See <code>data/geography/datasets/</code> in the repository.</p>";
  }
}

map.on("load", () => {
  addWorldLayer();
  resolveMapReady();
  setStatus("World ready · select France to enter the wine atlas");
});

map.on("click", "france-country-fill", () => {
  if (state.context === "world") enterFrance();
});
map.on("mouseenter", "france-country-fill", () => { map.getCanvas().style.cursor = "pointer"; });
map.on("mouseleave", "france-country-fill", () => { map.getCanvas().style.cursor = ""; });

map.on("click", (event) => {
  if (!state.franceLoaded) return;
  const layers = INTERACTIVE_LAYERS.filter((layer) => map.getLayer(layer) && map.getLayoutProperty(layer, "visibility") !== "none");
  if (state.igpLoaded && map.getLayoutProperty("igp-areas-fill", "visibility") !== "none") layers.push("igp-areas-fill");
  const features = map.queryRenderedFeatures(event.point, { layers });
  if (!features.length) return;
  const unique = [...new Map(features.map((feature) => [feature.properties.source_denomination_id || feature.properties.source_feature_id, feature])).values()];
  const primary = unique[0];
  const bounds = normalizeBounds(primary.properties.bounds);
  if (primary.layer.id === "wine-region-labels" && bounds) map.fitBounds(bounds, { padding: panelPadding(), maxZoom: 7.4, duration: 700 });
  openDetails(primary, unique);
});

map.on("mousemove", (event) => {
  if (!state.franceLoaded) return;
  const layers = INTERACTIVE_LAYERS.filter((layer) => map.getLayer(layer));
  map.getCanvas().style.cursor = map.queryRenderedFeatures(event.point, { layers }).length ? "pointer" : "";
});

map.on("error", () => { setStatus("Map context is partially unavailable · thematic data remains local"); });

document.querySelector("[data-explore-france]").addEventListener("click", () => enterFrance());
document.querySelector("[data-world]").addEventListener("click", returnToWorld);
document.querySelector("[data-close-detail]").addEventListener("click", closeDetails);

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
  await enterFrance({ fit: state.context !== "france" });
  setLayerVisibility(["aoc-areas-fill", "aoc-areas-line", "aoc-complements-fill", "aoc-labels"], elements.aocToggle.checked);
});
elements.igpToggle.addEventListener("change", async () => {
  if (elements.igpToggle.checked) await ensureIgpData();
  setLayerVisibility(["igp-areas-fill"], elements.igpToggle.checked);
});
elements.regionsToggle.addEventListener("change", async () => {
  await enterFrance({ fit: state.context !== "france" });
  setLayerVisibility(["wine-region-labels"], elements.regionsToggle.checked);
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

document.addEventListener("keydown", (event) => {
  if (event.key === "/" && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) {
    event.preventDefault();
    elements.searchInput.focus();
  }
  if (event.key === "Escape" && elements.detailPanel.classList.contains("is-open")) closeDetails();
});
document.addEventListener("click", (event) => { if (!elements.searchForm.contains(event.target)) closeSearch(); });

document.querySelector("[data-sources-button]").addEventListener("click", async () => {
  await renderSources();
  elements.sourcesDialog.showModal();
});
document.querySelector("[data-close-sources]").addEventListener("click", () => elements.sourcesDialog.close());
elements.sourcesDialog.addEventListener("click", (event) => { if (event.target === elements.sourcesDialog) elements.sourcesDialog.close(); });

window.addEventListener("resize", () => map.resize());

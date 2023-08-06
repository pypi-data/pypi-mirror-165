(self["webpackChunkipysigma"] = self["webpackChunkipysigma"] || []).push([["lib_widget_js"],{

/***/ "./lib/custom-hover.js":
/*!*****************************!*\
  !*** ./lib/custom-hover.js ***!
  \*****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
const label_1 = __importDefault(__webpack_require__(/*! sigma/rendering/canvas/label */ "./node_modules/sigma/rendering/canvas/label.js"));
/**
 * Draw an hovered node.
 * - if there is no label => display a shadow on the node
 * - if the label box is bigger than node size => display a label box that contains the node with a shadow
 * - else node with shadow and the label box
 */
function drawHover(context, data, settings) {
    const size = settings.labelSize, font = settings.labelFont, weight = settings.labelWeight;
    data = Object.assign(Object.assign({}, data), { label: data.label || data.hoverLabel });
    context.font = `${weight} ${size}px ${font}`;
    // Then we draw the label background
    context.fillStyle = '#FFF';
    context.shadowOffsetX = 0;
    context.shadowOffsetY = 0;
    context.shadowBlur = 8;
    context.shadowColor = '#000';
    const PADDING = 2;
    if (typeof data.label === 'string') {
        const textWidth = context.measureText(data.label).width, boxWidth = Math.round(textWidth + 5), boxHeight = Math.round(size + 2 * PADDING), radius = Math.max(data.size, size / 2) + PADDING;
        const angleRadian = Math.asin(boxHeight / 2 / radius);
        const xDeltaCoord = Math.sqrt(Math.abs(Math.pow(radius, 2) - Math.pow(boxHeight / 2, 2)));
        context.beginPath();
        context.moveTo(data.x + xDeltaCoord, data.y + boxHeight / 2);
        context.lineTo(data.x + radius + boxWidth, data.y + boxHeight / 2);
        context.lineTo(data.x + radius + boxWidth, data.y - boxHeight / 2);
        context.lineTo(data.x + xDeltaCoord, data.y - boxHeight / 2);
        context.arc(data.x, data.y, radius, angleRadian, -angleRadian);
        context.closePath();
        context.fill();
    }
    else {
        context.beginPath();
        context.arc(data.x, data.y, data.size + PADDING, 0, Math.PI * 2);
        context.closePath();
        context.fill();
    }
    context.shadowOffsetX = 0;
    context.shadowOffsetY = 0;
    context.shadowBlur = 0;
    // And finally we draw the label
    (0, label_1.default)(context, data, settings);
}
exports["default"] = drawHover;
//# sourceMappingURL=custom-hover.js.map

/***/ }),

/***/ "./lib/icons.js":
/*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
/***/ ((__unused_webpack_module, exports) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.scatterIcon = exports.fullscreenExitIcon = exports.fullscreenEnterIcon = exports.pauseIcon = exports.playIcon = exports.resetLayoutIcon = exports.resetZoomIcon = exports.unzoomIcon = exports.zoomIcon = void 0;
exports.zoomIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"></path><path d="M12 10h-2v2H9v-2H7V9h2V7h1v2h2v1z"></path></svg>`;
exports.unzoomIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14zM7 9h5v1H7z"></path></svg>`;
exports.resetZoomIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><path d="M5 15H3v4c0 1.1.9 2 2 2h4v-2H5v-4zM5 5h4V3H5c-1.1 0-2 .9-2 2v4h2V5zm14-2h-4v2h4v4h2V5c0-1.1-.9-2-2-2zm0 16h-4v2h4c1.1 0 2-.9 2-2v-4h-2v4zM12 8c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm0 6c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"></path></svg>`;
exports.resetLayoutIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><path d="M7.11 8.53 5.7 7.11C4.8 8.27 4.24 9.61 4.07 11h2.02c.14-.87.49-1.72 1.02-2.47zM6.09 13H4.07c.17 1.39.72 2.73 1.62 3.89l1.41-1.42c-.52-.75-.87-1.59-1.01-2.47zm1.01 5.32c1.16.9 2.51 1.44 3.9 1.61V17.9c-.87-.15-1.71-.49-2.46-1.03L7.1 18.32zM13 4.07V1L8.45 5.55 13 10V6.09c2.84.48 5 2.94 5 5.91s-2.16 5.43-5 5.91v2.02c3.95-.49 7-3.85 7-7.93s-3.05-7.44-7-7.93z"></path></svg>`;
exports.playIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"></path></svg>`;
exports.pauseIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"></path></svg>`;
exports.fullscreenEnterIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"></path></svg>`;
exports.fullscreenExitIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><path d="M5 16h3v3h2v-5H5v2zm3-8H5v2h5V5H8v3zm6 11h2v-3h3v-2h-5v5zm2-11V5h-2v5h5V8h-3z"></path></svg>`;
exports.scatterIcon = `<svg width="20" height="20" focusable="false" viewBox="0 0 24 24"><circle cx="7" cy="14" r="3"></circle><circle cx="11" cy="6" r="3"></circle><circle cx="16.6" cy="17.6" r="3"></circle></svg>`;
//# sourceMappingURL=icons.js.map

/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.saveAsSVG = exports.saveAsGEXF = exports.saveAsJSON = exports.saveAsPNG = exports.renderAsDataURL = void 0;
const sigma_1 = __importDefault(__webpack_require__(/*! sigma */ "webpack/sharing/consume/default/sigma/sigma"));
const file_saver_1 = __importDefault(__webpack_require__(/*! file-saver */ "webpack/sharing/consume/default/file-saver/file-saver"));
const gexf = __importStar(__webpack_require__(/*! graphology-gexf/browser */ "./node_modules/graphology-gexf/browser/index.js"));
// @ts-ignore
const renderer_1 = __importDefault(__webpack_require__(/*! graphology-svg/renderer */ "./node_modules/graphology-svg/renderer.js"));
// @ts-ignore
const defaults_1 = __webpack_require__(/*! graphology-svg/defaults */ "./node_modules/graphology-svg/defaults.js");
// Taken and adapted from: https://github.com/jacomyal/sigma.js/blob/main/examples/png-snapshot/saveAsPNG.ts
function renderToAuxiliaryCanvas(renderer, inputLayers) {
    const { width, height } = renderer.getDimensions();
    // This pixel ratio is here to deal with retina displays.
    // Indeed, for dimensions W and H, on a retina display, the canvases
    // dimensions actually are 2 * W and 2 * H. Sigma properly deals with it, but
    // we need to readapt here:
    const pixelRatio = window.devicePixelRatio || 1;
    const tmpRoot = document.createElement('DIV');
    tmpRoot.style.width = `${width}px`;
    tmpRoot.style.height = `${height}px`;
    tmpRoot.style.position = 'absolute';
    tmpRoot.style.right = '101%';
    tmpRoot.style.bottom = '101%';
    document.body.appendChild(tmpRoot);
    // Instantiate sigma:
    const tmpRenderer = new sigma_1.default(renderer.getGraph(), tmpRoot, renderer.getSettings());
    // Copy camera and force to render now, to avoid having to wait the schedule /
    // debounce frame:
    tmpRenderer.getCamera().setState(renderer.getCamera().getState());
    tmpRenderer.refresh();
    // Create a new canvas, on which the different layers will be drawn:
    const canvas = document.createElement('CANVAS');
    canvas.setAttribute('width', width * pixelRatio + '');
    canvas.setAttribute('height', height * pixelRatio + '');
    const ctx = canvas.getContext('2d');
    // Draw a white background first:
    ctx.fillStyle = '#fff';
    ctx.fillRect(0, 0, width * pixelRatio, height * pixelRatio);
    // For each layer, draw it on our canvas:
    const canvases = tmpRenderer.getCanvases();
    const layers = inputLayers
        ? inputLayers.filter((id) => !!canvases[id])
        : Object.keys(canvases);
    layers.forEach((id) => {
        ctx.drawImage(canvases[id], 0, 0, width * pixelRatio, height * pixelRatio, 0, 0, width * pixelRatio, height * pixelRatio);
    });
    return [
        canvas,
        () => {
            // Cleanup:
            tmpRenderer.kill();
            tmpRoot.remove();
        },
    ];
}
function renderAsDataURL(renderer) {
    const [canvas, cleanup] = renderToAuxiliaryCanvas(renderer);
    const dataURL = canvas.toDataURL();
    cleanup();
    return dataURL;
}
exports.renderAsDataURL = renderAsDataURL;
function saveAsPNG(renderer) {
    const [canvas, cleanup] = renderToAuxiliaryCanvas(renderer);
    // Save the canvas as a PNG image:
    canvas.toBlob((blob) => {
        if (blob)
            file_saver_1.default.saveAs(blob, 'graph.png');
        cleanup();
    }, 'image/png');
}
exports.saveAsPNG = saveAsPNG;
function saveAsJSON(renderer) {
    const data = JSON.stringify(renderer.getGraph(), null, 2);
    file_saver_1.default.saveAs(new Blob([data], { type: 'application/json' }), 'graph.json');
}
exports.saveAsJSON = saveAsJSON;
function saveAsGEXF(renderer) {
    const data = gexf.write(renderer.getGraph());
    file_saver_1.default.saveAs(new Blob([data], { type: 'application/xml' }), 'graph.gexf');
}
exports.saveAsGEXF = saveAsGEXF;
function saveAsSVG(renderer) {
    const rendererSettings = renderer.getSettings();
    const settings = Object.assign({}, defaults_1.DEFAULTS);
    settings.nodes = {
        // @ts-ignore
        reducer: (_, n, a) => rendererSettings.nodeReducer(n, a),
        defaultColor: rendererSettings.defaultNodeColor,
    };
    settings.edges = {
        // @ts-ignore
        reducer: (_, e, a) => rendererSettings.edgeReducer(e, a),
        defaultColor: rendererSettings.defaultEdgeColor,
    };
    const data = (0, renderer_1.default)(renderer.getGraph(), settings);
    file_saver_1.default.saveAs(new Blob([data], { type: 'image/svg+xml' }), 'graph.svg');
}
exports.saveAsSVG = saveAsSVG;
//# sourceMappingURL=utils.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./lib/visual-variables.js":
/*!*********************************!*\
  !*** ./lib/visual-variables.js ***!
  \*********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.VisualVariableScalesBuilder = exports.CategorySummary = exports.AttributeCategories = exports.AttributeExtents = exports.Extent = void 0;
const multi_set_1 = __importDefault(__webpack_require__(/*! mnemonist/multi-set */ "./node_modules/mnemonist/multi-set.js"));
const palette_1 = __importDefault(__webpack_require__(/*! iwanthue/palette */ "./node_modules/iwanthue/palette.js"));
const d3_scale_1 = __webpack_require__(/*! d3-scale */ "webpack/sharing/consume/default/d3-scale/d3-scale");
/**
 * Constants.
 */
const CATEGORY_MAX_COUNT = 10;
/**
 * Helper functions.
 */
function isValidNumber(value) {
    return typeof value === 'number' && !Number.isNaN(value);
}
/**
 * Helper classes.
 */
class Extent {
    constructor() {
        this.min = Infinity;
        this.max = -Infinity;
    }
    add(value) {
        if (value < this.min)
            this.min = value;
        if (value > this.max)
            this.max = value;
    }
    isConstant() {
        return this.min === Infinity || this.min === this.max;
    }
}
exports.Extent = Extent;
class AttributeExtents {
    constructor(names) {
        this.attributes = {};
        // NOTE: this naturally deduplicates names
        names.forEach((name) => (this.attributes[name] = new Extent()));
    }
    add(attributes) {
        for (const name in this.attributes) {
            const value = attributes[name];
            if (!isValidNumber(value))
                continue;
            this.attributes[name].add(value);
        }
    }
}
exports.AttributeExtents = AttributeExtents;
class AttributeCategories {
    constructor(names) {
        this.attributes = {};
        // NOTE: this naturally deduplicates names
        names.forEach((name) => (this.attributes[name] = new multi_set_1.default()));
    }
    add(attributes) {
        for (const name in this.attributes) {
            this.attributes[name].add(attributes[name]);
        }
    }
}
exports.AttributeCategories = AttributeCategories;
class CategorySummary {
    constructor(name, palette, overflowing = false) {
        this.name = name;
        this.palette = palette;
        this.overflowing = overflowing;
    }
    static fromTopValues(name, frequencies, defaultColor, maxCount = CATEGORY_MAX_COUNT) {
        const count = Math.min(maxCount, frequencies.dimension);
        const topValues = frequencies.top(count);
        const overflowing = count < frequencies.dimension;
        const values = topValues.map((item) => item[0]);
        const palette = palette_1.default.generateFromValues(name, values, { defaultColor });
        return new CategorySummary(name, palette, overflowing);
    }
    static fromColorEntries(name, entries, defaultColor) {
        const palette = palette_1.default.fromEntries(name, entries, defaultColor);
        return new CategorySummary(name, palette);
    }
}
exports.CategorySummary = CategorySummary;
class VisualVariableScalesBuilder {
    constructor(visualVariables, maxCategoryColors = CATEGORY_MAX_COUNT) {
        this.variables = visualVariables;
        this.maxCategoryColors = maxCategoryColors;
        const nodeExtentAttributes = [];
        const nodeCategoryAttributes = [];
        const edgeExtentAttributes = [];
        const edgeCategoryAttributes = [];
        for (const variableName in visualVariables) {
            const variable = visualVariables[variableName];
            if (variableName.startsWith('node')) {
                if (variable.type === 'category') {
                    if (!variable.palette)
                        nodeCategoryAttributes.push(variable.attribute);
                }
                else if (variable.type === 'continuous') {
                    nodeExtentAttributes.push(variable.attribute);
                }
            }
            else if (variableName.startsWith('edge')) {
                if (variable.type === 'category') {
                    if (!variable.palette)
                        edgeCategoryAttributes.push(variable.attribute);
                }
                else if (variable.type === 'continuous') {
                    if (variable.range[0] !== variable.range[1])
                        edgeExtentAttributes.push(variable.attribute);
                }
            }
        }
        this.nodeExtents = new AttributeExtents(nodeExtentAttributes);
        this.edgeExtents = new AttributeExtents(edgeExtentAttributes);
        this.nodeCategories = new AttributeCategories(nodeCategoryAttributes);
        this.edgeCategories = new AttributeCategories(edgeCategoryAttributes);
    }
    readGraph(graph) {
        graph.forEachNode((node, attr) => {
            this.nodeExtents.add(attr);
            this.nodeCategories.add(attr);
        });
        graph.forEachEdge((edge, attr) => {
            this.edgeExtents.add(attr);
            this.edgeCategories.add(attr);
        });
    }
    build() {
        const scales = {};
        for (const variableName in this.variables) {
            const variable = this.variables[variableName];
            let scale = null;
            // Raw variables
            if (variable.type === 'raw') {
                scale = (attr) => attr[variable.attribute] || variable.default;
            }
            // Category variables
            else if (variable.type === 'category') {
                const categories = variableName.startsWith('node')
                    ? this.nodeCategories
                    : this.edgeCategories;
                const summary = variable.palette
                    ? CategorySummary.fromColorEntries(variable.attribute, variable.palette, variable.default || '#ccc')
                    : CategorySummary.fromTopValues(variable.attribute, categories.attributes[variable.attribute], variable.default || '#ccc', this.maxCategoryColors);
                const palette = summary.palette;
                scale = (attr) => palette.get(attr[variable.attribute]);
                scale.summary = summary;
            }
            // Continuous variables
            else if (variable.type === 'continuous') {
                const extents = variableName.startsWith('node')
                    ? this.nodeExtents
                    : this.edgeExtents;
                const extent = extents.attributes[variable.attribute];
                if (variable.range[0] === variable.range[1] || extent.isConstant()) {
                    scale = () => variable.range[0];
                }
                else {
                    const continuousScale = (0, d3_scale_1.scaleLinear)()
                        .domain([extent.min, extent.max])
                        .range(variable.range);
                    scale = (attr) => continuousScale(attr[variable.attribute]);
                }
            }
            if (scale)
                scales[variableName] = scale;
        }
        return scales;
    }
    inferLabelRenderedSizeThreshold() {
        const attribute = this.variables.nodeSize.attribute;
        const extent = this.nodeExtents.attributes[attribute];
        return Math.min(6, extent.max);
    }
}
exports.VisualVariableScalesBuilder = VisualVariableScalesBuilder;
//# sourceMappingURL=visual-variables.js.map

/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.SigmaView = exports.SigmaModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const graphology_1 = __importDefault(__webpack_require__(/*! graphology */ "webpack/sharing/consume/default/graphology/graphology"));
const worker_1 = __importDefault(__webpack_require__(/*! graphology-layout-forceatlas2/worker */ "./node_modules/graphology-layout-forceatlas2/worker.js"));
const worker_2 = __importDefault(__webpack_require__(/*! graphology-layout-noverlap/worker */ "./node_modules/graphology-layout-noverlap/worker.js"));
const graphology_layout_forceatlas2_1 = __importDefault(__webpack_require__(/*! graphology-layout-forceatlas2 */ "webpack/sharing/consume/default/graphology-layout-forceatlas2/graphology-layout-forceatlas2"));
const graphology_communities_louvain_1 = __importDefault(__webpack_require__(/*! graphology-communities-louvain */ "webpack/sharing/consume/default/graphology-communities-louvain/graphology-communities-louvain"));
const utils_1 = __webpack_require__(/*! graphology-layout/utils */ "./node_modules/graphology-layout/utils.js");
const sigma_1 = __importDefault(__webpack_require__(/*! sigma */ "webpack/sharing/consume/default/sigma/sigma"));
const animate_1 = __webpack_require__(/*! sigma/utils/animate */ "./node_modules/sigma/utils/animate.js");
const settings_1 = __webpack_require__(/*! sigma/settings */ "./node_modules/sigma/settings.js");
const edge_fast_1 = __importDefault(__webpack_require__(/*! sigma/rendering/webgl/programs/edge.fast */ "./node_modules/sigma/rendering/webgl/programs/edge.fast.js"));
const edge_triangle_1 = __importDefault(__webpack_require__(/*! sigma/rendering/webgl/programs/edge.triangle */ "./node_modules/sigma/rendering/webgl/programs/edge.triangle.js"));
const border_1 = __importDefault(__webpack_require__(/*! @yomguithereal/sigma-experiments-renderers/node/border */ "./node_modules/@yomguithereal/sigma-experiments-renderers/node/border.js"));
const events_1 = __importDefault(__webpack_require__(/*! events */ "./node_modules/events/events.js"));
const seedrandom_1 = __importDefault(__webpack_require__(/*! seedrandom */ "webpack/sharing/consume/default/seedrandom/seedrandom"));
const comma_number_1 = __importDefault(__webpack_require__(/*! comma-number */ "webpack/sharing/consume/default/comma-number/comma-number"));
const choices_js_1 = __importDefault(__webpack_require__(/*! choices.js */ "webpack/sharing/consume/default/choices.js/choices.js"));
const screenfull_1 = __importDefault(__webpack_require__(/*! screenfull */ "webpack/sharing/consume/default/screenfull/screenfull"));
const debounce_1 = __importDefault(__webpack_require__(/*! debounce */ "webpack/sharing/consume/default/debounce/debounce"));
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const custom_hover_1 = __importDefault(__webpack_require__(/*! ./custom-hover */ "./lib/custom-hover.js"));
const visual_variables_1 = __webpack_require__(/*! ./visual-variables */ "./lib/visual-variables.js");
const utils_2 = __webpack_require__(/*! ./utils */ "./lib/utils.js");
const icons_1 = __webpack_require__(/*! ./icons */ "./lib/icons.js");
__webpack_require__(/*! choices.js/public/assets/styles/choices.min.css */ "./node_modules/choices.js/public/assets/styles/choices.min.css");
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
/**
 * Constants.
 */
const NODE_VIZ_ATTRIBUTES = new Set(['label', 'size', 'color', 'x', 'y']);
const EDGE_VIZ_ATTRIBUTES = new Set(['label', 'size', 'color']);
const MUTED_NODE_COLOR = '#ccc';
/**
 * Template.
 */
const TEMPLATE = `
<div class="ipysigma-container"></div>
<div class="ipysigma-left-panel">
  <div class="ipysigma-graph-description"></div>
  <div>
    <button class="ipysigma-zoom-button ipysigma-button ipysigma-svg-icon" title="zoom">
      ${icons_1.zoomIcon}
    </button>
    <button class="ipysigma-unzoom-button ipysigma-button ipysigma-svg-icon" title="unzoom">
      ${icons_1.unzoomIcon}
    </button>
    <button class="ipysigma-reset-zoom-button ipysigma-button ipysigma-svg-icon" title="reset zoom">
      ${icons_1.resetZoomIcon}
    </button>
  </div>
  <div>
    <button class="ipysigma-fullscreen-button ipysigma-button ipysigma-svg-icon" title="enter fullscreen">
      ${icons_1.fullscreenEnterIcon}
    </button>
  </div>
  <div class="ipysigma-layout-controls">
    <button class="ipysigma-layout-button ipysigma-button ipysigma-svg-icon" title="start layout">
      ${icons_1.playIcon}
    </button>
    <button class="ipysigma-noverlap-button ipysigma-button ipysigma-svg-icon" title="spread nodes">
      ${icons_1.scatterIcon}
    </button>
    <button class="ipysigma-reset-layout-button ipysigma-button ipysigma-svg-icon" title="reset layout">
      ${icons_1.resetLayoutIcon}
    </button>
  </div>
</div>
<div class="ipysigma-right-panel">
  <select class="ipysigma-search">
    <option value="">Search a node...</option>
  </select>
  <div class="ipysigma-information-shadow-display" style="display: none;">
    <span class="ipysigma-information-show-button">show legend</span>
  </div>
  <div class="ipysigma-information-display">
    <div class="ipysigma-information-display-tabs">
      <span class="ipysigma-information-legend-button ipysigma-tab-button">legend</span>
      &middot;
      <span class="ipysigma-information-info-button ipysigma-tab-button">info</span>
      <span class="ipysigma-information-hide-button">hide</span>
    </div>
    <hr>
    <div class="ipysigma-legend"></div>
    <div class="ipysigma-information-contents"></div>
  </div>
  <div class="ipysigma-download-controls">
    <button class="ipysigma-download-png-button ipysigma-button">
      png
    </button>
    <button class="ipysigma-download-svg-button ipysigma-button">
      svg
    </button>
    <button class="ipysigma-download-gexf-button ipysigma-button">
      gexf
    </button>
    <button class="ipysigma-download-json-button ipysigma-button">
      json
    </button>
  </div>
</div>
`;
/**
 * Model declaration.
 */
class SigmaModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: SigmaModel.model_name, _model_module: SigmaModel.model_module, _model_module_version: SigmaModel.model_module_version, _view_name: SigmaModel.view_name, _view_module: SigmaModel.view_module, _view_module_version: SigmaModel.view_module_version, data: { nodes: [], edges: [] }, height: 500, start_layout: false, snapshot: null, layout: null, clickableEdges: false, visual_variables: {} });
    }
}
exports.SigmaModel = SigmaModel;
SigmaModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
SigmaModel.model_name = 'SigmaModel';
SigmaModel.model_module = version_1.MODULE_NAME;
SigmaModel.model_module_version = version_1.MODULE_VERSION;
SigmaModel.view_name = 'SigmaView'; // Set to null if no view
SigmaModel.view_module = version_1.MODULE_NAME; // Set to null if no view
SigmaModel.view_module_version = version_1.MODULE_VERSION;
/**
 * Helper functions.
 */
function createRng() {
    return (0, seedrandom_1.default)('ipysigma');
}
function isValidNumber(value) {
    return typeof value === 'number' && !isNaN(value);
}
function escapeHtml(unsafe) {
    return ('' + unsafe)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
function renderTypedValue(value) {
    const safe = escapeHtml('' + value);
    let type = 'unknown';
    if (typeof value === 'number') {
        type = 'number';
    }
    else if (typeof value === 'string') {
        type = 'string';
    }
    else if (typeof value === 'boolean') {
        type = 'boolean';
    }
    return `<span class="ipysigma-${type}" title="${type}">${safe}</span>`;
}
function buildGraph(data, rng) {
    const graph = graphology_1.default.from(data);
    // Rectifications
    graph.updateEachNodeAttributes((key, attr) => {
        // Random position for nodes without positions
        if (!isValidNumber(attr.x))
            attr.x = rng();
        if (!isValidNumber(attr.y))
            attr.y = rng();
        return attr;
    });
    return graph;
}
function createElement(tag, options) {
    const element = document.createElement(tag);
    const { className, style, innerHTML, title } = options || {};
    if (className)
        element.setAttribute('class', className);
    for (const prop in style) {
        element.style[prop] = style[prop];
    }
    if (innerHTML)
        element.innerHTML = innerHTML;
    if (title)
        element.setAttribute('title', title);
    return element;
}
function hide(el) {
    el.style.display = 'none';
}
function show(el) {
    el.style.display = 'block';
}
function disable(el) {
    el.classList.add('disabled');
    el.disabled = true;
}
function enable(el) {
    el.classList.remove('disabled');
    el.disabled = false;
}
const SPINNER_STATES = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷'];
function createSpinner() {
    const span = createElement('span', {
        className: 'ipysigma-spinner',
        innerHTML: SPINNER_STATES[0],
    });
    let state = -1;
    let frame = null;
    const update = () => {
        state++;
        state %= SPINNER_STATES.length;
        span.innerHTML = SPINNER_STATES[state];
        frame = setTimeout(update, 80);
    };
    update();
    return [span, () => frame !== null && clearTimeout(frame)];
}
function getGraphDescription(graph) {
    let graphTitle = `${graph.multi ? 'Multi ' : ''}${graph.type === 'undirected' ? 'Undirected' : 'Directed'} Graph`;
    let html = `<u>${graphTitle}</u><br><b>${(0, comma_number_1.default)(graph.order)}</b> nodes<br><b>${(0, comma_number_1.default)(graph.size)}</b> edges`;
    return html;
}
const SYNC_REGISTRY = new Map();
/**
 * View declaration.
 */
class SigmaView extends base_1.DOMWidgetView {
    constructor() {
        super(...arguments);
        this.emitter = new events_1.default();
        this.edgeWeightAttribute = null;
        this.syncHoveredNode = null;
        this.syncListeners = {};
        this.layoutSpinner = null;
        this.currentTab = 'legend';
        this.isInformationShown = true;
        this.selectedNode = null;
        this.selectedEdge = null;
        this.focusedNodes = null;
        this.selectedNodeCategoryValues = null;
        this.selectedEdgeCategoryValues = null;
    }
    render() {
        super.render();
        this.el.classList.add('ipysigma-widget');
        const height = this.model.get('height');
        const data = this.model.get('data');
        const graph = buildGraph(data, createRng());
        this.graph = graph;
        // Preexisting layout?
        const preexistingLayout = this.model.get('layout');
        if (preexistingLayout) {
            (0, utils_1.assignLayout)(graph, preexistingLayout);
        }
        else {
            this.saveLayout();
        }
        this.originalLayoutPositions = (0, utils_1.collectLayout)(graph);
        // Selection state
        const selectedNodeCategoryValues = this.model.get('selected_node_category_values');
        const selectedEdgeCategoryValues = this.model.get('selected_edge_category_values');
        if (selectedNodeCategoryValues)
            this.selectedNodeCategoryValues = new Set(selectedNodeCategoryValues);
        if (selectedEdgeCategoryValues)
            this.selectedEdgeCategoryValues = new Set(selectedEdgeCategoryValues);
        // Widget-side metrics
        this.edgeWeightAttribute = this.model.get('edge_weight');
        let nodeMetrics = this.model.get('node_metrics') || {};
        // NOTE: for some untractable reason, I need a completly new deep object
        nodeMetrics = JSON.parse(JSON.stringify(nodeMetrics));
        for (const attrName in nodeMetrics) {
            const metricSpec = nodeMetrics[attrName];
            const metric = metricSpec.name;
            if (metric === 'louvain') {
                const communities = (0, graphology_communities_louvain_1.default)(graph, {
                    getEdgeWeight: this.edgeWeightAttribute,
                    rng: createRng(),
                    resolution: metricSpec.resolution || 1,
                });
                metricSpec.result = communities;
                graph.updateEachNodeAttributes((node, attr) => {
                    attr[attrName] = communities[node];
                    return attr;
                }, { attributes: [attrName] });
            }
            else {
                throw new Error(`unkown metric "${metric}"` + metric);
            }
        }
        this.model.set('node_metrics', nodeMetrics);
        this.touch();
        this.el.insertAdjacentHTML('beforeend', TEMPLATE);
        this.el.style.width = '100%';
        this.el.style.height = height + 'px';
        this.container = this.el.querySelector('.ipysigma-container');
        this.container.style.width = '100%';
        this.container.style.height = height + 'px';
        // Description
        const description = this.el.querySelector('.ipysigma-graph-description');
        description.innerHTML = getGraphDescription(graph);
        // Camera controls
        this.zoomButton = this.el.querySelector('.ipysigma-zoom-button');
        this.unzoomButton = this.el.querySelector('.ipysigma-unzoom-button');
        this.resetZoomButton = this.el.querySelector('.ipysigma-reset-zoom-button');
        // Fullscreen controls
        this.fullscreenButton = this.el.querySelector('.ipysigma-fullscreen-button');
        // Layout controls
        this.layoutControls = this.el.querySelector('.ipysigma-layout-controls');
        this.layoutButton = this.el.querySelector('.ipysigma-layout-button');
        this.noverlapButton = this.el.querySelector('.ipysigma-noverlap-button');
        this.resetLayoutButton = this.el.querySelector('.ipysigma-reset-layout-button');
        // Search
        var searchContainer = this.el.querySelector('.ipysigma-search');
        const nodeLabelAttribute = this.model.get('visual_variables').nodeLabel.attribute;
        const options = graph.mapNodes((key, attr) => {
            let labelParts = [escapeHtml(key)];
            const label = attr[nodeLabelAttribute];
            if (label && label !== key) {
                labelParts.push(` <small style="font-size: 75%;">${escapeHtml(label)}</small>`);
            }
            return { value: key, label: labelParts.join(' ') };
        });
        this.choices = new choices_js_1.default(searchContainer, {
            allowHTML: true,
            removeItemButton: true,
            renderChoiceLimit: 10,
            choices: options,
            itemSelectText: '',
            position: 'bottom',
        });
        this.informationDisplayElement = this.el.querySelector('.ipysigma-information-display');
        this.informationShadowDisplayElement = this.el.querySelector('.ipysigma-information-shadow-display');
        this.itemInfoElement = this.el.querySelector('.ipysigma-information-contents');
        this.legendElement = this.el.querySelector('.ipysigma-legend');
        this.nodeInfoButton = this.el.querySelector('.ipysigma-information-info-button');
        this.legendButton = this.el.querySelector('.ipysigma-information-legend-button');
        this.hideInformationButton = this.el.querySelector('.ipysigma-information-hide-button');
        this.showInformationButton = this.el.querySelector('.ipysigma-information-show-button');
        this.changeInformationDisplayTab('legend');
        // Download controls
        this.downloadPNGButton = this.el.querySelector('.ipysigma-download-png-button');
        this.downloadGEXFButton = this.el.querySelector('.ipysigma-download-gexf-button');
        this.downloadSVGButton = this.el.querySelector('.ipysigma-download-svg-button');
        this.downloadJSONButton = this.el.querySelector('.ipysigma-download-json-button');
        // Waiting for widget to be mounted to register events
        this.displayed.then(() => {
            var _a, _b, _c;
            const clickableEdges = this.model.get('clickable_edges');
            const programSettings = this.model.get('program_settings');
            const visualVariables = this.model.get('visual_variables');
            const nodeBordersEnabled = visualVariables.nodeBorderColor.type !== 'disabled';
            const edgeProgramClasses = Object.assign(Object.assign({}, settings_1.DEFAULT_SETTINGS.edgeProgramClasses), { slim: edge_fast_1.default, triangle: edge_triangle_1.default });
            const nodeProgramClasses = Object.assign({}, settings_1.DEFAULT_SETTINGS.nodeProgramClasses);
            if (nodeBordersEnabled) {
                nodeProgramClasses.circle = (0, border_1.default)({
                    borderRatio: programSettings.nodeBorderRatio,
                });
            }
            let rendererSettings = this.model.get('renderer_settings');
            rendererSettings = Object.assign({ zIndex: true, enableEdgeClickEvents: clickableEdges, enableEdgeHoverEvents: clickableEdges, hoverRenderer: custom_hover_1.default, edgeProgramClasses,
                nodeProgramClasses }, rendererSettings);
            if (!rendererSettings.defaultEdgeType)
                rendererSettings.defaultEdgeType =
                    graph.type !== 'undirected' ? 'arrow' : 'line';
            // Gathering info about the graph to build reducers correctly
            const maxCategoryColors = this.model.get('max_category_colors');
            const scaleBuilder = new visual_variables_1.VisualVariableScalesBuilder(visualVariables, maxCategoryColors);
            scaleBuilder.readGraph(graph);
            if (!('labelRenderedSizeThreshold' in rendererSettings))
                rendererSettings.labelRenderedSizeThreshold =
                    scaleBuilder.inferLabelRenderedSizeThreshold();
            const scales = scaleBuilder.build();
            this.updateLegend(visualVariables, {
                nodeColor: (_a = scales.nodeColor) === null || _a === void 0 ? void 0 : _a.summary,
                nodeBorderColor: (_b = scales.nodeBorderColor) === null || _b === void 0 ? void 0 : _b.summary,
                edgeColor: (_c = scales.edgeColor) === null || _c === void 0 ? void 0 : _c.summary,
            });
            const nodeDisplayDataRegister = {};
            const nodeCategoryAttribute = visualVariables.nodeColor.type === 'category'
                ? visualVariables.nodeColor.attribute
                : null;
            const edgeCategoryAttribute = visualVariables.edgeColor.type === 'category'
                ? visualVariables.edgeColor.attribute
                : null;
            const edgeColorFrom = visualVariables.edgeColor.type === 'dependent'
                ? visualVariables.edgeColor.value
                : null;
            // Node reducer
            rendererSettings.nodeReducer = (node, data) => {
                const displayData = {
                    x: data.x,
                    y: data.y,
                };
                // Visual variables
                const categoryValue = nodeCategoryAttribute
                    ? data[nodeCategoryAttribute]
                    : null;
                if (categoryValue) {
                    displayData.categoryValue = categoryValue;
                }
                displayData.color = scales.nodeColor(data);
                displayData.size = scales.nodeSize(data);
                displayData.label = (scales.nodeLabel(data) || node);
                if (nodeBordersEnabled) {
                    displayData.borderColor = scales.nodeBorderColor(data);
                }
                // Transient state
                if (node === this.selectedNode || node === this.syncHoveredNode) {
                    displayData.highlighted = true;
                }
                if ((this.focusedNodes && !this.focusedNodes.has(node)) ||
                    (this.selectedNodeCategoryValues &&
                        !this.selectedNodeCategoryValues.has(categoryValue))) {
                    displayData.color = MUTED_NODE_COLOR;
                    displayData.zIndex = 0;
                    displayData.size = displayData.size ? displayData.size / 2 : 1;
                    displayData.hoverLabel = displayData.label;
                    displayData.label = '';
                    if (nodeBordersEnabled) {
                        displayData.borderColor = MUTED_NODE_COLOR;
                    }
                }
                else {
                    displayData.zIndex = 1;
                }
                nodeDisplayDataRegister[node] = displayData;
                return displayData;
            };
            // Edge reducer
            rendererSettings.edgeReducer = (edge, data) => {
                var _a, _b;
                const displayData = {};
                const [source, target] = graph.extremities(edge);
                // Visual variables
                const categoryValue = edgeCategoryAttribute
                    ? data[edgeCategoryAttribute]
                    : null;
                if (edgeColorFrom) {
                    displayData.color =
                        nodeDisplayDataRegister[edgeColorFrom === 'source' ? source : target].color;
                }
                else {
                    displayData.color = scales.edgeColor(data);
                }
                displayData.size = scales.edgeSize(data);
                if (scales.edgeLabel)
                    displayData.label = scales.edgeLabel(data);
                // Transient state
                if (this.selectedNode && this.focusedNodes) {
                    if (source !== this.selectedNode && target !== this.selectedNode) {
                        displayData.hidden = true;
                    }
                }
                if (this.selectedNodeCategoryValues) {
                    if (!this.selectedNodeCategoryValues.has((_a = nodeDisplayDataRegister[source]) === null || _a === void 0 ? void 0 : _a.categoryValue) &&
                        !this.selectedNodeCategoryValues.has((_b = nodeDisplayDataRegister[target]) === null || _b === void 0 ? void 0 : _b.categoryValue)) {
                        displayData.hidden = true;
                    }
                }
                if (this.selectedEdgeCategoryValues) {
                    if (!this.selectedEdgeCategoryValues.has(categoryValue)) {
                        displayData.hidden = true;
                    }
                }
                if (this.selectedEdge) {
                    displayData.hidden = edge !== this.selectedEdge;
                }
                return displayData;
            };
            this.renderer = new sigma_1.default(graph, this.container, rendererSettings);
            const initialCameraState = this.model.get('camera_state');
            this.renderer.getCamera().setState(initialCameraState);
            const selectedNode = this.model.get('selected_node');
            const selectedEdge = this.model.get('selected_edge');
            if (selectedNode)
                this.selectItem('node', selectedNode);
            else if (selectedEdge)
                this.selectItem('edge', graph.edge(selectedEdge[0], selectedEdge[1]));
            else
                this.clearSelectedItem();
            this.bindMessageHandlers();
            this.bindRendererHandlers();
            this.bindChoicesHandlers();
            this.bindInformationDisplayHandlers();
            this.bindDownloadHandlers();
            this.bindCameraHandlers();
            this.bindFullscreenHandlers();
            this.bindLayoutHandlers();
            this.syncKey = this.model.get('sync_key');
            if (this.syncKey) {
                const currentSyncEntry = SYNC_REGISTRY.get(this.syncKey);
                if (!currentSyncEntry) {
                    const emitter = new events_1.default();
                    SYNC_REGISTRY.set(this.syncKey, {
                        emitter,
                        renderers: new Set([this.renderer]),
                    });
                    this.bindSyncEvents(emitter);
                }
                else {
                    currentSyncEntry.renderers.add(this.renderer);
                    this.bindSyncEvents(currentSyncEntry.emitter);
                }
            }
        });
    }
    renderSnapshot() {
        this.model.set('snapshot', (0, utils_2.renderAsDataURL)(this.renderer));
        this.touch();
    }
    saveCameraState(state) {
        this.model.set('camera_state', state);
        this.touch();
    }
    saveLayout() {
        const mapping = (0, utils_1.collectLayout)(this.graph);
        this.model.set('layout', mapping);
        this.touch();
    }
    resetLayout() {
        this.model.set('layout', this.originalLayoutPositions);
        this.touch();
    }
    changeInformationDisplayTab(tab) {
        if (tab === 'legend') {
            hide(this.itemInfoElement);
            show(this.legendElement);
            this.legendButton.classList.remove('selectable');
            this.nodeInfoButton.classList.add('selectable');
        }
        else {
            hide(this.legendElement);
            show(this.itemInfoElement);
            this.legendButton.classList.add('selectable');
            this.nodeInfoButton.classList.remove('selectable');
        }
    }
    toggleInformationDisplay() {
        if (this.isInformationShown) {
            // Hiding
            hide(this.informationDisplayElement);
            show(this.informationShadowDisplayElement);
            this.isInformationShown = false;
        }
        else {
            // Showing
            show(this.informationDisplayElement);
            hide(this.informationShadowDisplayElement);
            this.isInformationShown = true;
        }
    }
    updateLegend(variables, summaries) {
        const categoryMap = new Map();
        let dataId = 0;
        function renderLegend(type, title, variable, summary, defaultColor) {
            if (variable.type === 'disabled')
                return null;
            let html = `<b>${title}</b><br>`;
            if (variable.type === 'dependent') {
                html += `based on <span class="ipysigma-keyword">${variable.value}</span> color`;
            }
            else {
                const source = variable.attribute.startsWith('$$')
                    ? 'kwarg'
                    : 'attribute';
                const name = variable.attribute.startsWith('$$')
                    ? variable.attribute.slice(2)
                    : variable.attribute;
                if (variable.type === 'raw') {
                    html += `<span class="ipysigma-keyword">${escapeHtml(name)}</span> ${source}`;
                }
                else if (variable.type === 'continuous') {
                    html += `<span class="ipysigma-keyword">${escapeHtml(name)}</span> ${source} `;
                    if (typeof variable.range[0] === 'number') {
                        html += `(scaled to <span class="ipysigma-number">${variable.range[0]}</span>-<span class="ipysigma-number">${variable.range[1]}</span> px)`;
                    }
                    else {
                        html += `(from <span style="color: ${variable.range[0]}">■</span> ${variable.range[0]} to <span style="color: ${variable.range[1]}">■</span> ${variable.range[1]})`;
                    }
                }
                else {
                    html += `<span class="ipysigma-keyword">${escapeHtml(name)}</span> ${source} as a category:`;
                    const paletteItems = [];
                    if (summary) {
                        const values = [];
                        categoryMap.set(dataId, { type, values });
                        let i = 0;
                        summary.palette.forEach((color, value) => {
                            values.push(value);
                            paletteItems.push(`<span title="click to filter" class="category" data-key="${dataId}" data-index="${i++}"><span style="color: ${color}">■</span> <span class="category-value">${value}</span></span>`);
                        });
                        dataId++;
                        if (summary.overflowing) {
                            paletteItems.push(`<span style="color: ${summary.palette.defaultColor}">■</span> ...`);
                        }
                    }
                    else {
                        paletteItems.push(`<span style="color: ${defaultColor}">■</span> default`);
                    }
                    html += '<br>' + paletteItems.join('<br>');
                }
            }
            return html;
        }
        const items = [
            renderLegend('node', 'Node labels', variables.nodeLabel),
            renderLegend('node', 'Node colors', variables.nodeColor, summaries.nodeColor),
            renderLegend('node', 'Node border colors', variables.nodeBorderColor, summaries.nodeBorderColor),
            renderLegend('node', 'Node sizes', variables.nodeSize),
            renderLegend('edge', 'Edge colors', variables.edgeColor, summaries.edgeColor),
            renderLegend('edge', 'Edge sizes', variables.edgeSize),
            renderLegend('edge', 'Edge labels', variables.edgeLabel),
        ];
        this.legendElement.innerHTML = items.filter((l) => l).join('<hr>');
        // Binding category span events
        function getSpanInfo(span) {
            const key = +span.getAttribute('data-key');
            const index = +span.getAttribute('data-index');
            const record = categoryMap.get(key);
            if (!record)
                throw new Error('error registering category span click event handlers');
            return { type: record.type, value: record.values[index] };
        }
        const categorySpans = this.legendElement.querySelectorAll('.category');
        const updateSpans = () => {
            categorySpans.forEach((span) => {
                const { type, value } = getSpanInfo(span);
                if (type === 'node') {
                    if (!this.selectedNodeCategoryValues ||
                        this.selectedNodeCategoryValues.has(value)) {
                        span.classList.remove('evicted');
                    }
                    else {
                        span.classList.add('evicted');
                    }
                }
                else if (type === 'edge') {
                    if (!this.selectedEdgeCategoryValues ||
                        this.selectedEdgeCategoryValues.has(value)) {
                        span.classList.remove('evicted');
                    }
                    else {
                        span.classList.add('evicted');
                    }
                }
            });
        };
        categorySpans.forEach((span) => {
            span.onclick = () => {
                const { type, value } = getSpanInfo(span);
                const relatedPaletteCount = (type === 'node' ? summaries.nodeColor : summaries.edgeColor);
                this.toggleCategoryValue(type, relatedPaletteCount.palette.size, value);
                updateSpans();
                this.renderer.refresh();
            };
        });
        updateSpans();
    }
    clearSelectedItem() {
        this.selectedEdge = null;
        this.selectedNode = null;
        this.focusedNodes = null;
        this.syncHoveredNode = null;
        this.choices.setChoiceByValue('');
        if (this.model.get('clickable_edges')) {
            this.itemInfoElement.innerHTML =
                '<i>Click on a node/edge or search a node to display information about it...</i>';
        }
        else {
            this.itemInfoElement.innerHTML =
                '<i>Click on a node or search a node to display information about it...</i>';
        }
        this.changeInformationDisplayTab('legend');
        this.model.set('selected_node', null);
        this.model.set('selected_edge', null);
        this.touch();
        this.renderer.refresh();
        this.emitter.emit('clearSelectedItem');
    }
    toggleCategoryValue(type, max, value) {
        let target = type === 'node'
            ? this.selectedNodeCategoryValues
            : this.selectedEdgeCategoryValues;
        if (!target) {
            target = new Set([value]);
        }
        else if (target.size === max - 1) {
            target = null;
        }
        else if (target.has(value)) {
            if (target.size === 1) {
                target = null;
            }
            else {
                target.delete(value);
            }
        }
        else {
            target.add(value);
        }
        const update = target ? Array.from(target) : null;
        if (type === 'node') {
            this.selectedNodeCategoryValues = target;
            this.model.set('selected_node_category_values', update);
        }
        else {
            this.selectedEdgeCategoryValues = target;
            this.model.set('selected_edge_category_values', update);
        }
        this.touch();
    }
    selectItem(type, key) {
        const graph = this.graph;
        if (type === 'node') {
            this.selectedEdge = null;
            this.selectedNode = key;
            const focusedNodes = new Set();
            focusedNodes.add(this.selectedNode);
            graph.forEachNeighbor(key, (neighbor) => {
                focusedNodes.add(neighbor);
            });
            this.focusedNodes = focusedNodes;
            this.choices.setChoiceByValue(key);
            this.model.set('selected_node', key);
            this.model.set('selected_edge', null);
        }
        else {
            const extremities = graph.extremities(key);
            this.selectedEdge = key;
            this.selectedNode = null;
            this.focusedNodes = new Set(extremities);
            this.choices.setChoiceByValue('');
            this.model.set('selected_edge', extremities);
            this.model.set('selected_node', null);
        }
        this.touch();
        const attr = type === 'node'
            ? graph.getNodeAttributes(key)
            : graph.getEdgeAttributes(key);
        let innerHTML = '';
        if (type === 'node') {
            innerHTML += `<b>Node</b> <i>${renderTypedValue(key)}</i>`;
        }
        else {
            const [source, target] = this.graph.extremities(key);
            innerHTML += '<b>Edge</b>';
            if (!key.startsWith('geid_'))
                innerHTML += ` <i>${renderTypedValue(key)}</i>`;
            innerHTML += `<br>from ${renderTypedValue(source)} to ${renderTypedValue(target)}`;
        }
        const kwargInfo = [];
        const vizInfo = [];
        const info = [];
        const vizAttributes = type === 'node' ? NODE_VIZ_ATTRIBUTES : EDGE_VIZ_ATTRIBUTES;
        for (let k in attr) {
            let target = info;
            if (vizAttributes.has(k))
                target = vizInfo;
            else if (k.startsWith('$$'))
                target = kwargInfo;
            target.push(`<b>${k.startsWith('$$') ? k.slice(2) : k}</b> ${renderTypedValue(attr[k])}`);
        }
        if (kwargInfo.length !== 0)
            innerHTML += '<hr>From kwargs:<br>' + kwargInfo.join('<br>');
        if (info.length !== 0)
            innerHTML += `<hr>Attributes:<br>` + info.join('<br>');
        if (vizInfo.length !== 0)
            innerHTML += '<hr>Known viz data:<br>' + vizInfo.join('<br>');
        if (type === 'node') {
            innerHTML += '<hr>Computed metrics:<br>';
            innerHTML += `<b>degree</b> ${renderTypedValue(graph.degree(key))}<br>`;
            if (graph.directedSize !== 0) {
                innerHTML += `<b>indegree</b> ${renderTypedValue(graph.inDegree(key))}<br>`;
                innerHTML += `<b>outdegree</b> ${renderTypedValue(graph.outDegree(key))}<br>`;
            }
        }
        this.itemInfoElement.innerHTML = innerHTML;
        this.changeInformationDisplayTab('info');
        this.renderer.refresh();
        this.emitter.emit('selectItem', { type, key });
    }
    moveCameraToNode(node) {
        const pos = this.renderer.getNodeDisplayData(node);
        if (!pos)
            return;
        this.renderer.getCamera().animate(pos, { duration: 500 });
    }
    bindMessageHandlers() {
        this.model.on('msg:custom', (content) => {
            if (content.msg === 'render_snapshot') {
                this.renderSnapshot();
            }
        });
    }
    bindRendererHandlers() {
        const debouncedSaveCameraState = (0, debounce_1.default)(this.saveCameraState.bind(this), 500);
        this.renderer.getCamera().on('updated', (state) => {
            debouncedSaveCameraState(state);
        });
        this.renderer.on('enterNode', () => {
            this.container.style.cursor = 'pointer';
        });
        this.renderer.on('leaveNode', () => {
            this.container.style.cursor = 'default';
        });
        this.renderer.on('clickNode', ({ node }) => {
            if (node === this.selectedNode)
                return;
            this.selectItem('node', node);
        });
        this.renderer.on('clickStage', () => {
            if (!this.selectedNode && !this.selectedEdge)
                return;
            this.clearSelectedItem();
        });
        if (this.model.get('clickable_edges')) {
            this.renderer.on('enterEdge', () => {
                this.container.style.cursor = 'pointer';
            });
            this.renderer.on('leaveEdge', () => {
                this.container.style.cursor = 'default';
            });
            this.renderer.on('clickEdge', ({ edge }) => {
                if (edge === this.selectedEdge)
                    return;
                this.selectItem('edge', edge);
            });
        }
    }
    bindChoicesHandlers() {
        this.choices.passedElement.element.addEventListener('change', (event) => {
            const node = event.detail.value;
            if (node === this.selectedNode)
                return;
            if (!node)
                return this.clearSelectedItem();
            this.selectItem('node', node);
            // We don't need to move the camera if we are fully unzoomed
            if (this.renderer.getCamera().getState().ratio >= 1)
                return;
            this.moveCameraToNode(node);
        });
    }
    bindInformationDisplayHandlers() {
        this.legendButton.onclick = () => {
            if (!this.legendButton.classList.contains('selectable'))
                return;
            this.changeInformationDisplayTab('legend');
        };
        this.nodeInfoButton.onclick = () => {
            if (!this.nodeInfoButton.classList.contains('selectable'))
                return;
            this.changeInformationDisplayTab('info');
        };
        this.hideInformationButton.onclick = () => {
            this.toggleInformationDisplay();
        };
        this.showInformationButton.onclick = () => {
            this.toggleInformationDisplay();
        };
    }
    bindDownloadHandlers() {
        this.downloadPNGButton.onclick = () => {
            (0, utils_2.saveAsPNG)(this.renderer);
        };
        this.downloadGEXFButton.onclick = () => {
            (0, utils_2.saveAsGEXF)(this.renderer);
        };
        this.downloadSVGButton.onclick = () => {
            (0, utils_2.saveAsSVG)(this.renderer);
        };
        this.downloadJSONButton.onclick = () => {
            (0, utils_2.saveAsJSON)(this.renderer);
        };
    }
    bindCameraHandlers() {
        this.zoomButton.onclick = () => {
            this.renderer.getCamera().animatedZoom();
        };
        this.unzoomButton.onclick = () => {
            this.renderer.getCamera().animatedUnzoom();
        };
        this.resetZoomButton.onclick = () => {
            this.renderer.getCamera().animatedReset();
        };
    }
    bindFullscreenHandlers() {
        this.fullscreenButton.onclick = () => {
            if (screenfull_1.default.isFullscreen) {
                screenfull_1.default.exit().then(() => {
                    const targetHeight = this.model.get('height') + 'px';
                    this.el.style.height = targetHeight;
                    this.container.style.height = targetHeight;
                    this.fullscreenButton.innerHTML = icons_1.fullscreenEnterIcon;
                    this.fullscreenButton.setAttribute('title', 'enter fullscreen');
                    this.renderer.scheduleRefresh();
                });
            }
            else {
                screenfull_1.default.request(this.el).then(() => {
                    this.el.style.height = '100%';
                    this.container.style.height = '100%';
                    this.fullscreenButton.innerHTML = icons_1.fullscreenExitIcon;
                    this.fullscreenButton.setAttribute('title', 'exit fullscreen');
                    this.renderer.scheduleRefresh();
                });
            }
        };
    }
    bindLayoutHandlers() {
        const graph = this.graph;
        const renderer = this.renderer;
        let settings = (this.model.get('layout_settings') ||
            {});
        const inferredSettings = graphology_layout_forceatlas2_1.default.inferSettings(graph);
        settings = Object.assign(inferredSettings, settings);
        this.layout = new worker_1.default(graph, {
            settings,
            getEdgeWeight: this.edgeWeightAttribute,
        });
        this.noverlap = new worker_2.default(graph, {
            inputReducer(key, attr) {
                var _a;
                const pos = renderer.graphToViewport(attr);
                return {
                    x: pos.x,
                    y: pos.y,
                    size: (_a = renderer.getNodeDisplayData(key)) === null || _a === void 0 ? void 0 : _a.size,
                };
            },
            outputReducer(key, attr) {
                return renderer.viewportToGraph(attr);
            },
            onConverged() {
                stopNoverlap(true);
            },
            settings: { ratio: 1, margin: 3 },
        });
        hide(this.resetLayoutButton);
        const stopLayout = () => {
            if (this.layoutSpinner) {
                this.layoutControls.removeChild(this.layoutSpinner[0]);
                this.layoutSpinner[1]();
                this.layoutSpinner = null;
            }
            this.layoutButton.innerHTML = icons_1.playIcon;
            this.layoutButton.setAttribute('title', 'start layout');
            this.layout.stop();
            this.saveLayout();
            enable(this.noverlapButton);
            show(this.resetLayoutButton);
        };
        const startLayout = () => {
            this.layoutSpinner = createSpinner();
            this.layoutButton.innerHTML = icons_1.pauseIcon;
            this.layoutControls.appendChild(this.layoutSpinner[0]);
            this.layoutButton.setAttribute('title', 'stop layout');
            this.layout.start();
            disable(this.noverlapButton);
            hide(this.resetLayoutButton);
        };
        const stopNoverlap = (disableButton = false) => {
            if (this.layoutSpinner) {
                this.layoutControls.removeChild(this.layoutSpinner[0]);
                this.layoutSpinner[1]();
                this.layoutSpinner = null;
            }
            this.noverlapButton.innerHTML = icons_1.scatterIcon;
            this.noverlapButton.setAttribute('title', 'spread nodes');
            this.noverlap.stop();
            this.saveLayout();
            enable(this.layoutButton);
            show(this.resetLayoutButton);
            if (disableButton)
                disable(this.noverlapButton);
        };
        const startNoverlap = () => {
            this.layoutSpinner = createSpinner();
            this.noverlapButton.innerHTML = icons_1.pauseIcon;
            this.layoutControls.appendChild(this.layoutSpinner[0]);
            this.noverlapButton.setAttribute('title', 'stop');
            this.noverlap.start();
            disable(this.layoutButton);
            hide(this.resetLayoutButton);
        };
        const resetLayout = () => {
            enable(this.noverlapButton);
            hide(this.resetLayoutButton);
            this.resetLayout();
            (0, animate_1.animateNodes)(graph, this.originalLayoutPositions, { duration: 250 });
        };
        if (this.model.get('start_layout'))
            startLayout();
        this.layoutButton.onclick = () => {
            if (this.layout.isRunning()) {
                stopLayout();
            }
            else {
                startLayout();
            }
        };
        this.noverlapButton.onclick = () => {
            if (this.noverlap.isRunning()) {
                stopNoverlap();
            }
            else {
                startNoverlap();
            }
        };
        this.resetLayoutButton.onclick = () => {
            resetLayout();
        };
    }
    bindSyncEvents(syncEmitter) {
        let lock = false;
        // From the broadcaster's standpoint
        const camera = this.renderer.getCamera();
        camera.on('updated', (state) => {
            if (lock) {
                lock = false;
                return;
            }
            syncEmitter.emit('camera', { state, renderer: this.renderer });
        });
        const graph = this.renderer.getGraph();
        graph.on('nodeAttributesUpdated', ({ key, attributes }) => {
            if (lock) {
                lock = false;
                return;
            }
            syncEmitter.emit('nodePosition', {
                node: key,
                position: { x: attributes.x, y: attributes.y },
                renderer: this.renderer,
            });
        });
        graph.on('eachNodeAttributesUpdated', () => {
            if (lock) {
                lock = false;
                return;
            }
            syncEmitter.emit('layout', {
                layout: (0, utils_1.collectLayout)(graph),
                renderer: this.renderer,
            });
        });
        this.emitter.on('selectItem', (payload) => {
            if (lock) {
                lock = false;
                return;
            }
            syncEmitter.emit('selectItem', Object.assign(Object.assign({}, payload), { renderer: this.renderer }));
        });
        this.emitter.on('clearSelectedItem', () => {
            if (lock) {
                lock = false;
                return;
            }
            syncEmitter.emit('clearSelectedItem', { renderer: this.renderer });
        });
        this.renderer.on('enterNode', ({ node }) => {
            syncEmitter.emit('enterNode', { node, renderer: this.renderer });
        });
        this.renderer.on('leaveNode', ({ node }) => {
            syncEmitter.emit('leaveNode', { node, renderer: this.renderer });
        });
        // From the receiver's end
        this.syncListeners.camera = ({ state, renderer }) => {
            if (renderer === this.renderer)
                return;
            lock = true;
            camera.setState(state);
        };
        this.syncListeners.layout = ({ layout, renderer }) => {
            if (renderer === this.renderer)
                return;
            lock = true;
            (0, utils_1.assignLayout)(graph, layout);
        };
        this.syncListeners.nodePosition = ({ node, position, renderer }) => {
            if (renderer === this.renderer)
                return;
            lock = true;
            graph.mergeNodeAttributes(node, position);
        };
        this.syncListeners.enterNode = ({ node, renderer }) => {
            if (renderer === this.renderer)
                return;
            this.syncHoveredNode = node;
            this.renderer.scheduleRefresh();
        };
        this.syncListeners.leaveNode = ({ renderer }) => {
            if (renderer === this.renderer)
                return;
            this.syncHoveredNode = null;
            this.renderer.scheduleRefresh();
        };
        this.syncListeners.selectItem = ({ renderer, key, type }) => {
            if (renderer === this.renderer)
                return;
            lock = true;
            this.selectItem(type, key);
        };
        this.syncListeners.clearSelectedItem = ({ renderer }) => {
            if (renderer === this.renderer)
                return;
            lock = true;
            this.clearSelectedItem();
        };
        for (const eventName in this.syncListeners) {
            syncEmitter.on(eventName, this.syncListeners[eventName]);
        }
    }
    remove() {
        // Cleanup to avoid leaks and free GPU slots
        if (this.renderer)
            this.renderer.kill();
        if (this.layout)
            this.layout.kill();
        if (this.noverlap)
            this.noverlap.kill();
        if (this.syncKey) {
            const syncEntry = SYNC_REGISTRY.get(this.syncKey);
            if (!syncEntry) {
                throw new Error('sync entry not found on remove. this should not happen!');
            }
            if (syncEntry.renderers.size > 1) {
                syncEntry.renderers.delete(this.renderer);
                for (const eventName in this.syncListeners) {
                    syncEntry.emitter.removeListener(eventName, this.syncListeners[eventName]);
                }
            }
            else {
                syncEntry.emitter.removeAllListeners();
                SYNC_REGISTRY.delete(this.syncKey);
            }
        }
        this.emitter.removeAllListeners();
        super.remove();
    }
}
exports.SigmaView = SigmaView;
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, "/* Choices.js overrides */\n.choices {\n  margin-bottom: 5px;\n}\n\n.choices__inner {\n  border-radius: 0;\n  background-color: white;\n  border: 1px solid #e0e0e0;\n  box-sizing: border-box;\n}\n\n.choices__item--selectable {\n  padding-right: 0px !important;\n}\n\n/* Ipysigma own styles */\n.ipysigma-widget {\n  background-color: white;\n  margin: 0;\n  padding: 0;\n  border: 1px solid #e0e0e0;\n  font-family: sans-serif;\n  color: black;\n}\n\n.ipysigma-widget ~ .ipysigma-widget {\n  border-left: none;\n}\n\n.ipysigma-widget hr {\n  height: 1px;\n  border: none;\n  background-color: #e0e0e0;\n  margin-top: 6px;\n  margin-bottom: 6px;\n}\n\n.ipysigma-widget .ipysigma-left-panel {\n  position: absolute;\n  top: 10px;\n  left: 10px;\n}\n\n.ipysigma-widget .ipysigma-right-panel {\n  position: absolute;\n  top: 10px;\n  right: 10px;\n  width: 250px;\n  height: 100%;\n}\n\n.ipysigma-widget .ipysigma-graph-description {\n  background-color: white;\n  border: 1px solid #e0e0e0;\n  padding: 5px 10px;\n  font-size: 12px;\n  /* font-style: italic; */\n  line-height: 16px;\n}\n\n.ipysigma-widget .ipysigma-button {\n  cursor: pointer;\n  text-align: center;\n  background-color: white;\n  border: 1px solid #e0e0e0;\n  user-select: none;\n}\n\n.ipysigma-widget .ipysigma-button.disabled {\n  border: none;\n  cursor: default;\n}\n\n.ipysigma-widget .ipysigma-button.disabled svg {\n  fill: #efefef;\n}\n\n.ipysigma-widget .ipysigma-button:hover {\n  border-color: grey;\n}\n\n.ipysigma-widget .ipysigma-svg-icon {\n  width: 32px;\n  height: 32px;\n  font-size: 24px;\n  line-height: 30px;\n  box-sizing: border-box;\n}\n\n.ipysigma-widget .ipysigma-zoom-button {\n  margin-top: 10px;\n}\n\n.ipysigma-widget .ipysigma-unzoom-button {\n  margin-top: 10px;\n}\n\n.ipysigma-widget .ipysigma-reset-zoom-button {\n  margin-top: 10px;\n}\n\n.ipysigma-widget .ipysigma-fullscreen-button {\n  margin-top: 10px;\n}\n\n.ipysigma-widget .ipysigma-layout-controls {\n  width: 100%;\n  margin-top: 10px;\n  display: flex;\n}\n\n.ipysigma-widget .ipysigma-reset-layout-button,\n.ipysigma-widget .ipysigma-noverlap-button {\n  margin-left: 4px;\n}\n\n.ipysigma-widget .ipysigma-spinner {\n  font-size: 20px;\n  padding-left: 5px;\n  line-height: 26px;\n}\n\n.ipysigma-widget .ipysigma-tab-button.selectable {\n  color: cornflowerblue;\n  text-decoration: underline;\n  cursor: pointer;\n}\n\n.ipysigma-widget .ipysigma-information-display {\n  width: 100%;\n  height: calc(100% - 45px - 5px - 20px - 25px);\n  overflow-y: auto;\n  background-color: white;\n  border: 1px solid #e0e0e0;\n  box-sizing: border-box;\n  font-size: 12px;\n  /* font-style: italic; */\n  line-height: 16px;\n  padding: 10px;\n}\n\n.ipysigma-widget .ipysigma-information-shadow-display {\n  width: 100%;\n  overflow-y: auto;\n  box-sizing: border-box;\n  font-size: 12px;\n  /* font-style: italic; */\n  line-height: 16px;\n  padding: 10px;\n}\n\n.ipysigma-widget .ipysigma-information-hide-button,\n.ipysigma-widget .ipysigma-information-show-button {\n  float: right;\n  cursor: pointer;\n}\n\n.ipysigma-widget .ipysigma-information-contents,\n.ipysigma-widget .ipysigma-legend {\n  font-family: monospace;\n}\n\n.ipysigma-widget .ipysigma-string {\n  color: #bc2828;\n}\n\n.ipysigma-widget .ipysigma-number {\n  color: #008800;\n}\n\n.ipysigma-widget .ipysigma-boolean,\n.ipysigma-widget .ipysigma-keyword {\n  color: #0457ab;\n}\n\n.ipysigma-widget .ipysigma-download-controls {\n  margin-top: 5px;\n  /* display: flex; */\n  text-align: right;\n  position: absolute;\n  bottom: 20px;\n  right: 0px;\n}\n\n.ipysigma-widget .ipysigma-download-png-button,\n.ipysigma-widget .ipysigma-download-svg-button,\n.ipysigma-widget .ipysigma-download-gexf-button {\n  margin-right: 3px;\n}\n\n.ipysigma-widget .category {\n  cursor: pointer;\n}\n.ipysigma-widget .category.evicted .category-value {\n  color: gray;\n  text-decoration: line-through;\n}\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"ipysigma","version":"0.18.0","description":"A Jupyter widget using sigma.js to render interactive networks.","keywords":["sigma","graph","jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/medialab/ipysigma","bugs":{"url":"https://github.com/medialab/ipysigma/issues"},"license":"MIT","author":{"name":"Yomguithereal","email":"guillaume.plique@sciencespo.fr"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/medialab/ipysigma"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf ipysigma/labextension","clean:nbextension":"rimraf ipysigma/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","@yomguithereal/sigma-experiments-renderers":"^0.1.0","choices.js":"^10.1.0","chroma-js":"^2.4.2","comma-number":"^2.1.0","d3-scale":"^4.0.2","debounce":"^1.2.1","file-saver":"^2.0.5","graphology":"^0.24.1","graphology-communities-louvain":"^2.0.0","graphology-gexf":"^0.10.1","graphology-layout":"^0.6.0","graphology-layout-forceatlas2":"0.9.1-zeroweights2","graphology-layout-noverlap":"^0.4.2","graphology-svg":"^0.1.3","iwanthue":"^2.0.0","mnemonist":"^0.39.1","screenfull":"^6.0.1","seedrandom":"^3.0.5","sigma":"^2.3.0"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/chroma-js":"^2.1.3","@types/comma-number":"^2.1.0","@types/d3-scale":"^4.0.2","@types/debounce":"^1.2.1","@types/file-saver":"^2.0.5","@types/jest":"^26.0.0","@types/seedrandom":"^3.0.2","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","csstype":"^3.0.10","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.6.2","webpack":"^5.0.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"ipysigma/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.85690b518c71ecc13552.js.map
/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/ImageUploaderInline.scss":
/*!**************************************!*\
  !*** ./src/ImageUploaderInline.scss ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n// extracted by mini-css-extract-plugin\n\n\n//# sourceURL=webpack://django-image-uploader-widget/./src/ImageUploaderInline.scss?");

/***/ }),

/***/ "./src/Icons/DeleteIcon.ts":
/*!*********************************!*\
  !*** ./src/Icons/DeleteIcon.ts ***!
  \*********************************/
/***/ ((__unused_webpack_module, exports) => {

eval("\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\nexports[\"default\"] = '<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 512 512\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xml:space=\"preserve\" width=\"100%\" height=\"100%\"><path xmlns=\"http://www.w3.org/2000/svg\" d=\"m289.94 256 95-95A24 24 0 0 0 351 127l-95 95-95-95a24 24 0 0 0-34 34l95 95-95 95a24 24 0 1 0 34 34l95-95 95 95a24 24 0 0 0 34-34z\"></path></svg>';\n\n\n//# sourceURL=webpack://django-image-uploader-widget/./src/Icons/DeleteIcon.ts?");

/***/ }),

/***/ "./src/Icons/PreviewIcon.ts":
/*!**********************************!*\
  !*** ./src/Icons/PreviewIcon.ts ***!
  \**********************************/
/***/ ((__unused_webpack_module, exports) => {

eval("\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\nexports[\"default\"] = '<svg xmlns=\"http://www.w3.org/2000/svg\" fill=\"currentColor\" class=\"bi bi-zoom-in\" viewBox=\"0 0 16 16\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xml:space=\"preserve\" width=\"100%\" height=\"100%\"><path xmlns=\"http://www.w3.org/2000/svg\" fill-rule=\"evenodd\" d=\"M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zM13 6.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0z\"></path><path xmlns=\"http://www.w3.org/2000/svg\" d=\"M10.344 11.742c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1 6.538 6.538 0 0 1-1.398 1.4z\"></path><path xmlns=\"http://www.w3.org/2000/svg\" fill-rule=\"evenodd\" d=\"M6.5 3a.5.5 0 0 1 .5.5V6h2.5a.5.5 0 0 1 0 1H7v2.5a.5.5 0 0 1-1 0V7H3.5a.5.5 0 0 1 0-1H6V3.5a.5.5 0 0 1 .5-.5z\"></path></svg>';\n\n\n//# sourceURL=webpack://django-image-uploader-widget/./src/Icons/PreviewIcon.ts?");

/***/ }),

/***/ "./src/ImageUploaderInline.ts":
/*!************************************!*\
  !*** ./src/ImageUploaderInline.ts ***!
  \************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

eval("\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\nconst Editor_1 = __webpack_require__(/*! ./Inline/Editor */ \"./src/Inline/Editor.ts\");\ndocument.addEventListener('DOMContentLoaded', () => {\n    Array\n        .from(document.querySelectorAll('.iuw-inline-root'))\n        .map((element) => new Editor_1.ImageUploaderInline(element));\n});\n\n\n//# sourceURL=webpack://django-image-uploader-widget/./src/ImageUploaderInline.ts?");

/***/ }),

/***/ "./src/Inline/Editor.ts":
/*!******************************!*\
  !*** ./src/Inline/Editor.ts ***!
  \******************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

eval("\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\nexports.ImageUploaderInline = void 0;\nconst Utils_1 = __webpack_require__(/*! ./Utils */ \"./src/Inline/Utils.ts\");\nconst EditorImage_1 = __webpack_require__(/*! ./EditorImage */ \"./src/Inline/EditorImage.ts\");\nclass ImageUploaderInline {\n    constructor(element) {\n        this.handleImageDelete = (image) => {\n            var _a;\n            if (image.element.getAttribute('data-raw')) {\n                image.element.classList.add('deleted');\n                const checkboxInput = image.element.querySelector('input[type=checkbox]');\n                checkboxInput.checked = true;\n            }\n            else {\n                (_a = image.element.parentElement) === null || _a === void 0 ? void 0 : _a.removeChild(image.element);\n            }\n            this.images = this.images.filter((item) => item !== image);\n            this.updateEmpty();\n        };\n        this.handleDrop = (e) => {\n            var _a;\n            e.preventDefault();\n            this.element.classList.remove('drop-zone');\n            if ((_a = e.dataTransfer) === null || _a === void 0 ? void 0 : _a.files.length) {\n                for (const file of e.dataTransfer.files) {\n                    this.addFile(file);\n                }\n            }\n        };\n        this.handleDragEnter = () => {\n            this.element.classList.add('drop-zone');\n        };\n        this.handleDragOver = (e) => {\n            if (e) {\n                e.preventDefault();\n            }\n        };\n        this.handleDragLeave = (e) => {\n            if (e.relatedTarget && e.relatedTarget.closest('.iuw-inline-root') === this.element) {\n                return;\n            }\n            this.element.classList.remove('drop-zone');\n        };\n        this.canPreview = true;\n        this.tempFileInput = null;\n        this.element = element;\n        this.inlineGroup = (0, Utils_1.getInlineGroupOrThrow)(this.element);\n        this.inlineFormset = (0, Utils_1.parseFormSet)(this.inlineGroup);\n        this.management = (0, Utils_1.getManagementInputs)(this.inlineFormset.options.prefix);\n        this.next = 0;\n        if (this.management.maxNumForms.value === '') {\n            this.maxCount = Number.MAX_SAFE_INTEGER;\n        }\n        else {\n            this.maxCount = parseInt(this.management.maxNumForms.value, 10);\n        }\n        this.addImageButton = (0, Utils_1.getAddButton)(this.element);\n        this.updateEmpty();\n        this.updateAllIndexes();\n        this.images = Array\n            .from(this.element.querySelectorAll('.inline-related'))\n            .map((item) => {\n            const editorImage = new EditorImage_1.EditorImage(item, this.canPreview);\n            editorImage.onDelete = this.handleImageDelete;\n            return editorImage;\n        });\n        this.bindVariables();\n        this.bindEvents();\n        this.element.addEventListener('dragenter', this.handleDragEnter);\n        this.element.addEventListener('dragover', this.handleDragOver);\n        this.element.addEventListener('dragleave', this.handleDragLeave);\n        this.element.addEventListener('dragend', this.handleDragLeave);\n        this.element.addEventListener('drop', this.handleDrop);\n    }\n    bindVariables() {\n        this.handleAddImage = this.handleAddImage.bind(this);\n        this.handleTempFileInputChange = this.handleTempFileInputChange.bind(this);\n    }\n    bindEvents() {\n        var _a;\n        this.addImageButton.addEventListener('click', this.handleAddImage);\n        (_a = this.element.querySelector('.iuw-empty')) === null || _a === void 0 ? void 0 : _a.addEventListener('click', this.handleAddImage);\n    }\n    updateEmpty() {\n        const { length } = this.element.querySelectorAll('.inline-related:not(.empty-form):not(.deleted)');\n        this.element.classList.toggle('non-empty', length > 0);\n    }\n    updateAllIndexes() {\n        const { prefix } = this.inlineFormset.options;\n        const { length: count } = Array\n            .from(this.element.querySelectorAll('.inline-related:not(.empty-form)'))\n            .map((item, index) => {\n            (0, Utils_1.updateAllElementsIndexes)(item, prefix, index);\n            return item;\n        });\n        this.next = count;\n        this.management.totalForms.value = String(this.next);\n        this.addImageButton.classList.toggle('visible-by-number', this.maxCount - this.next > 0);\n    }\n    createFromEmptyTemplate() {\n        var _a;\n        const template = this.element.querySelector('.inline-related.empty-form');\n        if (!template) {\n            throw new Error('no-empty-template');\n        }\n        const row = template.cloneNode(true);\n        row.classList.remove('empty-form');\n        row.classList.remove('last-related');\n        row.setAttribute('data-candelete', 'true');\n        row.id = `${this.inlineFormset.options.prefix}-${this.next}`;\n        (_a = template.parentElement) === null || _a === void 0 ? void 0 : _a.insertBefore(row, template);\n        return row;\n    }\n    addFile(fileToAdd = null) {\n        var _a;\n        const row = this.createFromEmptyTemplate();\n        let file = null;\n        if (fileToAdd) {\n            file = fileToAdd;\n            const rowFileInput = row.querySelector('input[type=file]');\n            const dataTransferList = new DataTransfer();\n            dataTransferList.items.add(file);\n            rowFileInput.files = dataTransferList.files;\n        }\n        else {\n            if (!this.tempFileInput) {\n                throw new Error('no-temp-input-for-upload');\n            }\n            file = (this.tempFileInput.files || [null])[0];\n            if (!file) {\n                throw new Error('no-file-in-input');\n            }\n            const rowFileInput = row.querySelector('input[type=file]');\n            const parent = rowFileInput.parentElement;\n            const className = rowFileInput.className;\n            const name = rowFileInput.getAttribute('name');\n            parent.removeChild(rowFileInput);\n            this.tempFileInput.className = className;\n            this.tempFileInput.setAttribute('name', name || '');\n            (_a = this.tempFileInput.parentElement) === null || _a === void 0 ? void 0 : _a.removeChild(this.tempFileInput);\n            parent.appendChild(this.tempFileInput);\n            this.tempFileInput = null;\n        }\n        const editorImage = new EditorImage_1.EditorImage(row, true, URL.createObjectURL(file));\n        editorImage.onDelete = this.handleImageDelete;\n        this.images.push(editorImage);\n        this.updateEmpty();\n        this.updateAllIndexes();\n    }\n    handleTempFileInputChange() {\n        var _a;\n        const filesList = (_a = this.tempFileInput) === null || _a === void 0 ? void 0 : _a.files;\n        if (!filesList || filesList.length <= 0) {\n            return;\n        }\n        this.addFile();\n    }\n    handleAddImage() {\n        if (!this.tempFileInput) {\n            this.tempFileInput = (0, Utils_1.createTempFileInput)();\n            this.tempFileInput.addEventListener('change', this.handleTempFileInputChange);\n            this.element.appendChild(this.tempFileInput);\n        }\n        this.tempFileInput.click();\n    }\n}\nexports.ImageUploaderInline = ImageUploaderInline;\n\n\n//# sourceURL=webpack://django-image-uploader-widget/./src/Inline/Editor.ts?");

/***/ }),

/***/ "./src/Inline/EditorImage.ts":
/*!***********************************!*\
  !*** ./src/Inline/EditorImage.ts ***!
  \***********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

eval("\nvar __importDefault = (this && this.__importDefault) || function (mod) {\n    return (mod && mod.__esModule) ? mod : { \"default\": mod };\n};\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\nexports.EditorImage = void 0;\nconst PreviewIcon_1 = __importDefault(__webpack_require__(/*! ../Icons/PreviewIcon */ \"./src/Icons/PreviewIcon.ts\"));\nconst DeleteIcon_1 = __importDefault(__webpack_require__(/*! ../Icons/DeleteIcon */ \"./src/Icons/DeleteIcon.ts\"));\nconst PreviewModal_1 = __webpack_require__(/*! ../PreviewModal */ \"./src/PreviewModal/index.ts\");\nclass EditorImage {\n    constructor(element, canPreview, newImage) {\n        this.element = element;\n        this.canPreview = canPreview;\n        this.onDelete = null;\n        this.handleClick = this.handleClick.bind(this);\n        this.handleInputChange = this.handleInputChange.bind(this);\n        if (!!newImage) {\n            this.render(newImage);\n        }\n        else {\n            const inputs = this.removeAndGetInputs();\n            const link = this.getAndUpdateRawImage();\n            this.element.innerHTML = '';\n            inputs.forEach((item) => this.element.appendChild(item));\n            this.render(link);\n        }\n    }\n    removeAndGetInputs() {\n        return Array\n            .from(this.element.querySelectorAll('input[type=hidden], input[type=checkbox], input[type=file]'))\n            .map((item) => {\n            var _a;\n            (_a = item.parentElement) === null || _a === void 0 ? void 0 : _a.removeChild(item);\n            return item;\n        });\n    }\n    getAndUpdateRawImage() {\n        let rawImage = document.querySelector('p.file-upload a');\n        if (this.element.classList.contains('empty-form')) {\n            rawImage = null;\n        }\n        let hrefAttr = null;\n        if (rawImage) {\n            hrefAttr = rawImage.getAttribute('href');\n            if (hrefAttr) {\n                this.element.setAttribute('data-raw', hrefAttr);\n            }\n        }\n        return hrefAttr;\n    }\n    render(link) {\n        var _a;\n        if (!link) {\n            return;\n        }\n        let delete_icon = null;\n        const related = this.element.closest('.inline-related');\n        related === null || related === void 0 ? void 0 : related.addEventListener('click', this.handleClick);\n        (_a = related === null || related === void 0 ? void 0 : related.querySelector('input[type=file]')) === null || _a === void 0 ? void 0 : _a.addEventListener('change', this.handleInputChange);\n        if ((related === null || related === void 0 ? void 0 : related.getAttribute('data-candelete')) === 'true') {\n            delete_icon = document.createElement('span');\n            delete_icon.classList.add('iuw-delete-icon');\n            delete_icon.innerHTML = DeleteIcon_1.default;\n        }\n        if (this.canPreview) {\n            const span = document.createElement('span');\n            span.classList.add('iuw-preview-icon');\n            if ((related === null || related === void 0 ? void 0 : related.getAttribute('data-candelete')) !== 'true') {\n                span.classList.add('iuw-only-preview');\n            }\n            span.innerHTML = PreviewIcon_1.default;\n            this.element.appendChild(span);\n        }\n        const img = document.createElement('img');\n        img.src = link;\n        this.element.appendChild(img);\n        if (delete_icon) {\n            this.element.appendChild(delete_icon);\n        }\n    }\n    handleClick(e) {\n        if (!e || !e.target) {\n            return;\n        }\n        const target = e.target;\n        const item = target.closest('.inline-related');\n        if (target.closest('.iuw-delete-icon') && !!this.onDelete) {\n            this.onDelete(this);\n            return;\n        }\n        if (target.closest('.iuw-preview-icon')) {\n            let image = item === null || item === void 0 ? void 0 : item.querySelector('img');\n            if (image) {\n                image = image.cloneNode(true);\n                PreviewModal_1.PreviewModal.createPreviewModal(image);\n                PreviewModal_1.PreviewModal.openPreviewModal();\n                return;\n            }\n        }\n        const fileInput = item === null || item === void 0 ? void 0 : item.querySelector('input[type=file]');\n        if (e.target === fileInput) {\n            return;\n        }\n        fileInput === null || fileInput === void 0 ? void 0 : fileInput.click();\n    }\n    handleInputChange(e) {\n        var _a;\n        if (!e || !e.target || e.target.tagName !== 'INPUT') {\n            return;\n        }\n        const fileInput = e.target;\n        var files = fileInput.files;\n        if (!(files === null || files === void 0 ? void 0 : files.length)) {\n            return;\n        }\n        const imgTag = (_a = fileInput.closest('.inline-related')) === null || _a === void 0 ? void 0 : _a.querySelector('img');\n        if (imgTag) {\n            imgTag.src = URL.createObjectURL(files[0]);\n        }\n    }\n}\nexports.EditorImage = EditorImage;\n\n\n//# sourceURL=webpack://django-image-uploader-widget/./src/Inline/EditorImage.ts?");

/***/ }),

/***/ "./src/Inline/Utils.ts":
/*!*****************************!*\
  !*** ./src/Inline/Utils.ts ***!
  \*****************************/
/***/ ((__unused_webpack_module, exports) => {

eval("\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\nexports.createTempFileInput = exports.getAddButton = exports.getManagementInputs = exports.updateAllElementsIndexes = exports.updateElementIndex = exports.parseFormSet = exports.getInlineGroupOrThrow = void 0;\nfunction getInlineGroupOrThrow(element) {\n    const inlineGroup = element.closest('.inline-group');\n    if (!inlineGroup) {\n        throw new Error('no-inline-group-found');\n    }\n    return inlineGroup;\n}\nexports.getInlineGroupOrThrow = getInlineGroupOrThrow;\nfunction parseFormSet(element) {\n    const formSetDataString = element.getAttribute('data-inline-formset');\n    if (!formSetDataString) {\n        throw new Error('no-formset-data-found');\n    }\n    return JSON.parse(formSetDataString);\n}\nexports.parseFormSet = parseFormSet;\nfunction updateElementIndex(element, prefix, index) {\n    const findRegex = new RegExp(`(${prefix}-(\\\\d+|__prefix__))`);\n    const replacement = `${prefix}-${index}`;\n    // replace at [for]\n    const forAttr = element.getAttribute('for');\n    if (forAttr) {\n        element.setAttribute('for', forAttr.replace(findRegex, replacement));\n    }\n    // replace at [id]\n    const idAttr = element.getAttribute('id');\n    if (idAttr) {\n        element.setAttribute('id', idAttr.replace(findRegex, replacement));\n    }\n    // replace at [name]\n    const nameAttr = element.getAttribute('name');\n    if (nameAttr) {\n        element.setAttribute('name', nameAttr.replace(findRegex, replacement));\n    }\n}\nexports.updateElementIndex = updateElementIndex;\nfunction updateAllElementsIndexes(element, prefix, index) {\n    updateElementIndex(element, prefix, index);\n    Array\n        .from(element.querySelectorAll('*'))\n        .forEach((childItem) => updateElementIndex(childItem, prefix, index));\n}\nexports.updateAllElementsIndexes = updateAllElementsIndexes;\nfunction getManagementInputs(prefix) {\n    const totalForms = document.querySelector(`#id_${prefix}-TOTAL_FORMS`);\n    const initialForms = document.querySelector(`#id_${prefix}-INITIAL_FORMS`);\n    const minNumForms = document.querySelector(`#id_${prefix}-MIN_NUM_FORMS`);\n    const maxNumForms = document.querySelector(`#id_${prefix}-MAX_NUM_FORMS`);\n    if (!totalForms || !initialForms || !minNumForms || !maxNumForms) {\n        throw new Error('management-forms-not-found');\n    }\n    return { totalForms, initialForms, minNumForms, maxNumForms };\n}\nexports.getManagementInputs = getManagementInputs;\nfunction getAddButton(element) {\n    const addImageButton = element.querySelector('.iuw-add-image-btn');\n    if (!addImageButton) {\n        throw new Error('no-add-button-found');\n    }\n    return addImageButton;\n}\nexports.getAddButton = getAddButton;\nfunction createTempFileInput() {\n    const tempFileInput = document.createElement('input');\n    tempFileInput.setAttribute('type', 'file');\n    tempFileInput.classList.add('temp_file');\n    tempFileInput.setAttribute('accept', 'image/*');\n    tempFileInput.style.display = 'none';\n    return tempFileInput;\n}\nexports.createTempFileInput = createTempFileInput;\n\n\n//# sourceURL=webpack://django-image-uploader-widget/./src/Inline/Utils.ts?");

/***/ }),

/***/ "./src/PreviewModal/PreviewModal.ts":
/*!******************************************!*\
  !*** ./src/PreviewModal/PreviewModal.ts ***!
  \******************************************/
/***/ ((__unused_webpack_module, exports) => {

eval("\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\nexports.PreviewModal = void 0;\nexports.PreviewModal = {\n    openPreviewModal: () => {\n        const modal = document.getElementById('iuw-modal-element');\n        if (!modal) {\n            return;\n        }\n        setTimeout(() => {\n            modal.classList.add('visible');\n            modal.classList.remove('hide');\n            document.body.style.overflow = 'hidden';\n        }, 50);\n    },\n    closePreviewModal: () => {\n        document.body.style.overflow = 'auto';\n        const modal = document.getElementById('iuw-modal-element');\n        if (modal) {\n            modal.classList.remove('visible');\n            modal.classList.add('hide');\n            setTimeout(() => {\n                var _a;\n                (_a = modal.parentElement) === null || _a === void 0 ? void 0 : _a.removeChild(modal);\n            }, 300);\n        }\n    },\n    onModalClick: (e) => {\n        if (e && e.target) {\n            const element = e.target;\n            if (element.closest('img.iuw-modal-image-preview-item')) {\n                return;\n            }\n        }\n        exports.PreviewModal.closePreviewModal();\n    },\n    createPreviewModal: (image) => {\n        image.className = '';\n        image.classList.add('iuw-modal-image-preview-item');\n        const modal = document.createElement('div');\n        modal.id = 'iuw-modal-element';\n        modal.classList.add('iuw-modal', 'hide');\n        modal.addEventListener('click', exports.PreviewModal.onModalClick);\n        const preview = document.createElement('div');\n        preview.classList.add('iuw-modal-image-preview');\n        preview.innerHTML = '<span class=\"iuw-modal-close\"><svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 512 512\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xml:space=\"preserve\" width=\"100%\" height=\"100%\"><path xmlns=\"http://www.w3.org/2000/svg\" d=\"m289.94 256 95-95A24 24 0 0 0 351 127l-95 95-95-95a24 24 0 0 0-34 34l95 95-95 95a24 24 0 1 0 34 34l95-95 95 95a24 24 0 0 0 34-34z\"></path></svg></span>';\n        preview.appendChild(image);\n        modal.appendChild(preview);\n        document.body.appendChild(modal);\n        return modal;\n    }\n};\n\n\n//# sourceURL=webpack://django-image-uploader-widget/./src/PreviewModal/PreviewModal.ts?");

/***/ }),

/***/ "./src/PreviewModal/index.ts":
/*!***********************************!*\
  !*** ./src/PreviewModal/index.ts ***!
  \***********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

eval("\nvar __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {\n    if (k2 === undefined) k2 = k;\n    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });\n}) : (function(o, m, k, k2) {\n    if (k2 === undefined) k2 = k;\n    o[k2] = m[k];\n}));\nvar __exportStar = (this && this.__exportStar) || function(m, exports) {\n    for (var p in m) if (p !== \"default\" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);\n};\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\n__exportStar(__webpack_require__(/*! ./PreviewModal */ \"./src/PreviewModal/PreviewModal.ts\"), exports);\n\n\n//# sourceURL=webpack://django-image-uploader-widget/./src/PreviewModal/index.ts?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	__webpack_require__("./src/ImageUploaderInline.ts");
/******/ 	var __webpack_exports__ = __webpack_require__("./src/ImageUploaderInline.scss");
/******/ 	
/******/ })()
;
/**
 * --------------------------------------------------------------------------
 * NJ: collapse.ts
 * --------------------------------------------------------------------------
 */
import { Core } from '../../globals/ts/enum';
import AbstractComponent from '../../globals/ts/abstract-component';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class Collapse extends AbstractComponent {
    static readonly NAME: string;
    static readonly DATA_KEY: string;
    protected static readonly EVENT_KEY: string;
    protected static readonly DATA_API_KEY = Core.KEY_PREFIX;
    static readonly CLASS_NAME: {
        show: string;
        collapse: string;
        collapsing: string;
        collapsed: string;
    };
    static readonly EVENT: {
        show: string;
        shown: string;
        hide: string;
        hidden: string;
        clickDataApi: string;
    };
    protected static readonly DEFAULT_OPTIONS: {
        toggle: boolean;
        parent: string;
    };
    private static readonly DEFAULT_TYPE;
    private static readonly DIMENSION;
    protected static readonly SELECTOR: {
        default: string;
        actives: string;
        dataToggle: string;
    };
    private isTransitioning;
    private triggerArray;
    private selector;
    private parent;
    constructor(element: HTMLElement, options?: {});
    toggle(): void;
    show(): void;
    hide(): void;
    setTransitioning(isTransitioning: boolean): void;
    dispose(): void;
    getDimension(): string;
    getParent(): HTMLElement;
    addAriaAndCollapsedClass(element: any, triggerArray: any): void;
    private static getOptions;
    static getTargetFromElement(element: any): Element | null;
    static collapseInterface(element: any, options: any): void;
    static getInstance(element: HTMLElement): Collapse;
    static init(options?: {}): Collapse[];
    /**
     * ------------------------------------------------------------------------
     * Data Api implementation
     * ------------------------------------------------------------------------
     */
    private registerEvents;
}
export declare class CollapseWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

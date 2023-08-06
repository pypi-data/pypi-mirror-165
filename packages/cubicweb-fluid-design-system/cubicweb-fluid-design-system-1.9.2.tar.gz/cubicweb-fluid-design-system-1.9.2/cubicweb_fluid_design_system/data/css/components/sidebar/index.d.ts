/**
 * --------------------------------------------------------------------------
 * NJ: sidebar.ts
 * --------------------------------------------------------------------------
 */
import { Core } from '../../globals/ts/enum';
import AbstractComponent from '../../globals/ts/abstract-component';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class Sidebar extends AbstractComponent {
    static readonly NAME: string;
    static readonly DATA_KEY: string;
    protected static readonly EVENT_KEY: string;
    protected static readonly DATA_API_KEY = Core.KEY_PREFIX;
    static readonly CLASS_NAME: {
        folding: string;
        folded: string;
    };
    static readonly EVENT: {
        show: string;
        shown: string;
        hide: string;
        hidden: string;
        clickDataApi: string;
    };
    protected static readonly DEFAULT_OPTIONS: {
        folded: boolean;
    };
    private static readonly DEFAULT_TYPE;
    protected static readonly SELECTOR: {
        default: string;
        actives: string;
        dataToggle: string;
    };
    private isTransitioning;
    private triggerArray;
    private selector;
    constructor(element: HTMLElement, options?: {});
    toggle(): void;
    open(): void;
    close(): void;
    setTransitioning(isTransitioning: boolean): void;
    dispose(): void;
    addAriaAndExpandedClass(element: any, triggerArray: any): void;
    private static getOptions;
    static getTargetFromElement(element: any): Element | null;
    static expandInterface(element: any, options: any): void;
    static getInstance(element: HTMLElement): Sidebar;
    static init(options?: {}): Sidebar[];
    /**
     * ------------------------------------------------------------------------
     * Data Api implementation
     * ------------------------------------------------------------------------
     */
    private registerEvents;
}
export declare class SidebarWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

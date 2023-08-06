/**
 * --------------------------------------------------------------------------
 * NJ: Tab.ts
 * --------------------------------------------------------------------------
 */
import AbstractComponent from '../../globals/ts/abstract-component';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class Tab extends AbstractComponent {
    static readonly NAME: string;
    static readonly DATA_KEY: string;
    static CLASS_NAME: {
        component: string;
        tabItem: string;
        focusActive: string;
        tabContent: string;
        itemActive: string;
        contentActive: string;
    };
    static SELECTOR: {
        default: string;
    };
    private readonly tabs;
    currentIndex: number;
    currentFocusIndex: number;
    constructor(element: HTMLElement, options?: {});
    show: (e: any) => void;
    onKeyDown: (e: KeyboardEvent) => void;
    focus: (e: any) => void;
    blur: (e: any) => void;
    dispose(): void;
    static getInstance(element: HTMLElement): Tab;
    static init(options?: {}): Tab[];
}
export declare class TabWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}
export declare const useTabAccessibility: void;

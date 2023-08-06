/**
 * --------------------------------------------------------------------------
 * NJ : Tag.ts
 * --------------------------------------------------------------------------
 */
import 'web-animations-js';
import AbstractComponent from '../../globals/ts/abstract-component';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class Tag extends AbstractComponent {
    static readonly NAME: string;
    protected static readonly DATA_KEY: string;
    protected static readonly KEYFRAMES: {
        opacity: number;
    }[];
    protected static readonly SELECTOR: {
        default: string;
    };
    constructor(element: HTMLElement, options?: {});
    close(): void;
    /**
     * Remove element from DOM
     * */
    destroyElement(): void;
    dispose(): void;
    handleClick(event: any): void;
    static init(options?: {}): Tag[];
    static getInstance(element: HTMLElement): Tag;
    static getRootElement(element: Element): Element;
}
export declare class TagWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

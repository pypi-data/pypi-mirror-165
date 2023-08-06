/**
 * --------------------------------------------------------------------------
 * NJ : Fab.ts
 * --------------------------------------------------------------------------
 */
import 'web-animations-js';
import AbstractComponent from '../../globals/ts/abstract-component';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class Fab extends AbstractComponent {
    static readonly NAME: string;
    protected static readonly DATA_KEY: string;
    protected static readonly EVENT_KEY: string;
    protected static readonly SELECTOR: {
        default: string;
        button: string;
        item: string;
    };
    private static readonly EVENT;
    private static readonly DURATION_PER_ITEM;
    private static readonly ITEMS_HEIGHT;
    private static readonly OPEN_CLASS;
    private static readonly STAGGER_DELAY;
    private buttons;
    private items;
    constructor(element: any, options: any);
    open(): void;
    setListeners(): void;
    setOptions(options: any): void;
    getOptions(): any;
    dispose(): void;
    static getInstance(element: HTMLElement): Fab;
    static init(options?: {}): Fab[];
}
export declare class FabWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

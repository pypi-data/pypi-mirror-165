/**
 * --------------------------------------------------------------------------
 * NJ: dropdown.ts
 * --------------------------------------------------------------------------
 */
import { Core } from '../../globals/ts/enum';
import AbstractComponent from '../../globals/ts/abstract-component';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class Dropdown extends AbstractComponent {
    static readonly NAME: string;
    protected static readonly DATA_KEY: string;
    protected static readonly EVENT_KEY: string;
    protected static readonly DATA_API_KEY = Core.KEY_PREFIX;
    private static readonly ESCAPE_KEYCODE;
    private static readonly ATTRIBUTE;
    private static readonly CLASS_NAME;
    protected static readonly SELECTOR: {
        default: string;
        input: string;
        label: string;
        options: string;
    };
    private static readonly EVENT;
    value: string;
    constructor(element: HTMLElement);
    closeMenu(): void;
    dispose(): void;
    static handleCollapseShow(event: any): void;
    static handleCollapseHide(event: any): void;
    static getInstance(element: HTMLElement): Dropdown;
    static init(options?: {}): Dropdown[];
    private addTouchEvent;
    private addBlurEvent;
    /**
     * ------------------------------------------------------------------------
     * Data Api implementation
     * ------------------------------------------------------------------------
     */
    private registerEvents;
}
export declare class DropdownWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

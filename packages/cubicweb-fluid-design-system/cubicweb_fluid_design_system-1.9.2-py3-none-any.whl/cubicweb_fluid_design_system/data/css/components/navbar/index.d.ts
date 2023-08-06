/**
 * --------------------------------------------------------------------------
 * NJ : Navbar.ts
 * --------------------------------------------------------------------------
 */
import AbstractComponent from '../../globals/ts/abstract-component';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class Navbar extends AbstractComponent {
    static readonly NAME: string;
    protected static readonly DATA_KEY: string;
    private static readonly CLASS_NAME;
    static readonly SELECTOR: {
        default: string;
    };
    private collapseSearchBarInstances;
    constructor(element: HTMLElement);
    dispose(): void;
    handleCollapseShow(): void;
    handleCollapseHide(): void;
    static getInstance(element: HTMLElement): Navbar;
    static init(options?: {}): Navbar[];
    /**
     * ------------------------------------------------------------------------
     * Data Api implementation
     * ------------------------------------------------------------------------
     */
    private registerEvents;
}
export declare class NavbarWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

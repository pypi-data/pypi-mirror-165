/**
 * --------------------------------------------------------------------------
 * NJ : Header.ts
 * --------------------------------------------------------------------------
 */
import AbstractComponent from '../../globals/ts/abstract-component';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class Header extends AbstractComponent {
    static readonly NAME: string;
    protected static readonly DATA_KEY: string;
    protected static readonly SELECTOR: {
        default: string;
    };
    private minimizeWindowHeightThreshold;
    private static readonly CLASS_NAME;
    private readonly menuBurger;
    private openSearch;
    constructor(element: HTMLElement);
    dispose(): void;
    static getInstance(element: HTMLElement): Header;
    static init(options?: {}): Header[];
    get minimizeThreshold(): number;
    set minimizeThreshold(value: number);
    minimize(): void;
    maximize(): void;
    togglePanelShow(e: any): void;
    closePanels(): void;
    closeCurrentPanel(e: any): void;
    resetPanels(): void;
    onScroll: import("../../globals/ts/util").ReturnFunction<import("../../globals/ts/util").ReturnFunction<void>>;
    focusSearchInput: () => void;
}
export declare class HeaderWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

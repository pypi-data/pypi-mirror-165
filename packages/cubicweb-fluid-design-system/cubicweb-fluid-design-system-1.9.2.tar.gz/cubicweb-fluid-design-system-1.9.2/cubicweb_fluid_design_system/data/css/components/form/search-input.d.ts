/**
 * --------------------------------------------------------------------------
 * NJ: search-input.ts
 * --------------------------------------------------------------------------
 */
import AbstractComponent from '../../globals/ts/abstract-component';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class SearchInput extends AbstractComponent {
    static readonly NAME: string;
    protected static readonly DATA_KEY: string;
    static readonly SELECTOR: {
        default: string;
    };
    private static readonly INPUT_CLASS;
    private static readonly RESET_CLASS;
    protected static readonly DEFAULT_OPTIONS: {
        selector: {
            default: string;
        };
    };
    constructor(element: HTMLElement, options?: {});
    static init(options?: {}): SearchInput[];
    dispose(): void;
    static getInstance(element: HTMLElement): SearchInput;
    private setListeners;
}
export declare class SearchInputWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

/**
 * --------------------------------------------------------------------------
 * NJ: password-input.ts
 * --------------------------------------------------------------------------
 */
import AbstractComponent from '../../globals/ts/abstract-component';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class PasswordInput extends AbstractComponent {
    static readonly NAME: string;
    protected static readonly DATA_KEY: string;
    static readonly SELECTOR: {
        default: string;
    };
    private static readonly INPUT_CLASS;
    private static readonly REVEAL_BUTTON_CLASS;
    private static readonly HIDE_BUTTON_CLASS;
    protected static readonly DEFAULT_OPTIONS: {
        selector: {
            default: string;
        };
    };
    constructor(element: HTMLElement, options?: {});
    static init(options?: {}): PasswordInput[];
    static getInstance(element: HTMLElement): PasswordInput;
    dispose(): void;
    private setListeners;
}
export declare class PasswordInputWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

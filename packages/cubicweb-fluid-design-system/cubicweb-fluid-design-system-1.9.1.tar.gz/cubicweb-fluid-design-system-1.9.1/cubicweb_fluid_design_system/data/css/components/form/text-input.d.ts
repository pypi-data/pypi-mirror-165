/**
 * --------------------------------------------------------------------------
 * NJ: text.ts
 * --------------------------------------------------------------------------
 */
import AbstractFormControl from '../../globals/ts/abstract-form-control';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class TextInput extends AbstractFormControl {
    static readonly NAME: string;
    protected static readonly DATA_KEY: string;
    static readonly SELECTOR: {
        default: string;
        formGroup: string;
    };
    protected static readonly DEFAULT_OPTIONS: {
        njFormGroup: {
            required: boolean;
        };
    };
    constructor(element: HTMLInputElement, options?: {});
    dispose(): void;
    static init(options?: {}): TextInput[];
    static getInstance(element: HTMLInputElement): TextInput;
    static matches(element: Element): boolean;
}
export declare class TextInputWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

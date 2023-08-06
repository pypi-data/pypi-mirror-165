/**
 * --------------------------------------------------------------------------
 * NJ: textarea.ts
 * --------------------------------------------------------------------------
 */
import AbstractFormControl from '../../globals/ts/abstract-form-control';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class TextareaInput extends AbstractFormControl {
    static readonly NAME: string;
    protected static readonly DATA_KEY: string;
    static readonly SELECTOR: {
        default: string;
        formGroup: string;
    };
    constructor(element: HTMLTextAreaElement, options?: {});
    dispose(): void;
    static init(options?: {}): TextareaInput[];
    static getInstance(element: HTMLTextAreaElement): TextareaInput;
    static matches(element: Element): boolean;
}
export declare class TextareaInputWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

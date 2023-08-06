/**
 * --------------------------------------------------------------------------
 * NJ : Checkbox.ts
 * --------------------------------------------------------------------------
 */
import AbstractFormBaseSelection from '../../globals/ts/abstract-form-base-selection';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class Checkbox extends AbstractFormBaseSelection {
    static readonly NAME: string;
    protected static readonly DATA_KEY: string;
    protected static readonly SELECTOR: {
        root: string;
        default: string;
        formGroup: string;
        label: string;
    };
    protected static readonly DEFAULT_OPTIONS: {
        template: string;
        njFormGroup: {
            required: boolean;
        };
    };
    constructor(element: HTMLInputElement, options?: {}, properties?: {});
    dispose(): void;
    static init(options?: {}): Checkbox[];
    static getInstance(element: HTMLInputElement): Checkbox;
    static matches(element: Element): boolean;
}
export declare class CheckboxWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

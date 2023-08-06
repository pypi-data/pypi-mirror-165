/**
 * --------------------------------------------------------------------------
 * NJ : Radio.ts
 * --------------------------------------------------------------------------
 */
import AbstractFormBaseSelection from '../../globals/ts/abstract-form-base-selection';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class Radio extends AbstractFormBaseSelection {
    static readonly NAME: string;
    protected static readonly DATA_KEY: string;
    protected static readonly SELECTOR: {
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
    constructor(element: HTMLInputElement, options?: {}, properties?: {
        inputType: string;
        outerClass: string;
    });
    dispose(): void;
    matches(): boolean;
    static getInstance(element: HTMLInputElement): Radio;
    static init(options?: {}): Radio[];
}
export declare class RadioWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

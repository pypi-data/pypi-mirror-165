/**
 * --------------------------------------------------------------------------
 * NJ : Select.ts
 * --------------------------------------------------------------------------
 */
import AbstractFormBaseInput from '../../globals/ts/abstract-form-base-input';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class Select extends AbstractFormBaseInput {
    static readonly NAME: string;
    protected static readonly DATA_KEY: string;
    protected static readonly SELECTOR: {
        default: string;
        formGroup: string;
    };
    protected static readonly DEFAULT_OPTIONS: any;
    constructor(element: HTMLSelectElement, options?: {});
    dispose(): void;
    static init(options?: {}): Select[];
    static getInstance(element: HTMLSelectElement): Select;
    static matches(element: any): boolean;
}
export declare class SelectWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

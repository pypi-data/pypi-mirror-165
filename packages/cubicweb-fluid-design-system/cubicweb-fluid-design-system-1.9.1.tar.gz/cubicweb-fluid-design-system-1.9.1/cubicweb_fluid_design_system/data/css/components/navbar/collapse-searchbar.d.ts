import AbstractFormBase from '../../globals/ts/abstract-form-base';
import Collapse from '../collapse';
export default class CollapseSearchBar extends AbstractFormBase {
    protected static readonly NAME = "collapseSearchBar";
    protected static readonly DATA_KEY: string;
    static readonly SELECTOR: {
        default: string;
        formGroup: string;
        anyInput: string;
        target: string;
    };
    protected static readonly DEFAULT_OPTIONS: {
        njFormGroup: {
            required: boolean;
        };
    };
    private triggerElement;
    private input;
    constructor(element: HTMLElement, options?: {});
    getElement(): HTMLElement;
    dispose(): void;
    static init(options?: {}): CollapseSearchBar[];
    static getInstance(element: HTMLElement): CollapseSearchBar | Collapse;
    dismissHandler(event: any): void;
}

/**
 * --------------------------------------------------------------------------
 * NJ: Slider.ts
 * --------------------------------------------------------------------------
 */
import AbstractComponent from '../../globals/ts/abstract-component';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class Slider extends AbstractComponent {
    static readonly NAME: string;
    protected static readonly DATA_KEY: string;
    private static readonly CLASS_NAME;
    protected static readonly SELECTOR: {
        default: string;
        input: string;
        label: string;
    };
    private static readonly THUMB_WIDTH;
    private static readonly DEFAULT_TYPE;
    protected static readonly DEFAULT_OPTIONS: {
        tooltip: boolean;
    };
    private static readonly PERCENT_CONV;
    private static readonly PSEUDO_ELEMS;
    private dataId;
    private input;
    private tooltip;
    constructor(element: HTMLElement, options?: {});
    private addTooltip;
    private setListeners;
    private setTooltipListeners;
    private refreshProgressValue;
    private refreshTooltipValue;
    private replaceTooltip;
    private static getOptions;
    dispose(): void;
    static getInstance(element: HTMLElement): Slider;
    static init(options?: {}): Slider[];
}
export declare class SliderWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

/**
 * --------------------------------------------------------------------------
 * NJ : Alert.ts
 * --------------------------------------------------------------------------
 */
import 'web-animations-js';
import AbstractComponent from '../../globals/ts/abstract-component';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class Alert extends AbstractComponent {
    static readonly NAME: string;
    protected static readonly DATA_KEY: string;
    protected static readonly EVENT_KEY: string;
    protected static readonly SELECTOR: {
        default: string;
        dismiss: string;
    };
    private static readonly KEY_FRAMES;
    private static readonly EVENT;
    constructor(element: HTMLElement);
    close(): void;
    dispose(): void;
    private destroyElement;
    private setListeners;
    static init(options?: {}): Alert[];
    static getInstance(element: HTMLElement): Alert;
}
export declare class AlertWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

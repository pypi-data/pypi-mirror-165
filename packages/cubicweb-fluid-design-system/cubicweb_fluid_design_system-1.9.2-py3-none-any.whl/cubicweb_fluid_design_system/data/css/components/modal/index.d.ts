import { Core } from '../../globals/ts/enum';
import AbstractComponent from '../../globals/ts/abstract-component';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class Modal extends AbstractComponent {
    static readonly NAME: string;
    protected static readonly DATA_KEY: string;
    protected static readonly EVENT_KEY: string;
    protected static readonly DATA_API_KEY = Core.KEY_PREFIX;
    private static readonly ESCAPE_KEYCODE;
    static CLASSNAME: {
        backdrop: string;
        fade: string;
        show: string;
        visible: string;
    };
    static SELECTOR: {
        default: string;
        dataDismiss: string;
        dataToggle: string;
        modalBody: string;
        dialog: string;
    };
    private static readonly EVENT;
    private backdrop;
    private dialog;
    private ignoreBackdropClick;
    private isShown;
    private isTransitioning;
    constructor(element: HTMLElement);
    static init(options?: {}): Modal[];
    static getInstance(element: HTMLElement): Modal;
    private enforceFocus;
    private hideModal;
    private removeBackdrop;
    private setEscapeEvent;
    private showBackdrop;
    private showElement;
    dispose(): void;
    hide(event?: Event): void;
    show(): void;
    toggle(): void;
    /**
     * ------------------------------------------------------------------------
     * Data Api implementation
     * ------------------------------------------------------------------------
     */
    private registerEvents;
}
export declare class ModalWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

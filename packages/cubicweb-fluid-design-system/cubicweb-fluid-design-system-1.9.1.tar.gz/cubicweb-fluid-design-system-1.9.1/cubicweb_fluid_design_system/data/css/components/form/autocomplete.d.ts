/**
 * --------------------------------------------------------------------------
 * NJ: autocomplete.ts
 * --------------------------------------------------------------------------
 */
import AbstractComponent from '../../globals/ts/abstract-component';
import WebComponentFactory from '../../globals/ts/web-component-factory';
export default class Autocomplete extends AbstractComponent {
    static readonly NAME: string;
    protected static readonly DATA_KEY: string;
    static readonly SELECTOR: {
        default: string;
        input: string;
        list: string;
        listGroup: string;
    };
    private dataList;
    private currentList;
    private readonly listFragment;
    options: {
        autocomplete: boolean;
        limit: number | boolean;
    };
    private root;
    constructor(element: HTMLElement, options?: {});
    static init(options?: {}): Autocomplete[];
    dispose(): void;
    set data(data: Array<{
        name: string;
        value: string;
    }>);
    get data(): Array<{
        name: string;
        value: string;
    }>;
    get list(): Array<{
        name: string;
        value: string;
    }>;
    set list(data: Array<{
        name: string;
        value: string;
    }>);
    private static compareText;
    onInputChange: () => void;
    onKeyDown: (e: any) => void;
    onSelectListItem: (e: any) => void;
    onUserSelectItem({ name, value }: {
        name: any;
        value: any;
    }): void;
    static getInstance(element: HTMLElement): Autocomplete;
}
export declare class AutocompleteWC extends WebComponentFactory {
    static readonly TAG_NAME: string;
    constructor();
    static init(): void;
}

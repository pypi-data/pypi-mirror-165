export default class Form {
    static TextInput: object;
    static SearchInput: object;
    static PasswordInput: object;
    static TextareaInput: object;
    static Autocomplete: object;
    protected static readonly SELECTOR: {
        default: string;
    };
    static init(optionsPassword?: {}, optionsSearch?: {}, optionsText?: {}, optionsTextarea?: {}): Form[];
}
export declare class FormWC {
    static init(): void;
}

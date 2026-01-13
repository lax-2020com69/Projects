import "./Input.css";
type Inputprops = {
    id:string;
    name?:string;
    type:"number" | "text" |"email";
    value:string;
    placeholder?:string;
    className?:string;
    onChange?:(e:React.ChangeEvent<HTMLInputElement>) => void;
    disabled?:boolean;
    required?: boolean;
};
const Input:React.FC<Inputprops> = ({id, name, type, value, placeholder, className, onChange, disabled, required}) => {
  return (
    <div>
        <input
        id={id}
        name={name}
        type={type}
        value={value}
        placeholder={placeholder}
        className={`trainee-inputs ${className || ""}`}
        onChange={onChange}
        disabled={disabled}
        required={required}
        />
    </div>
  )
}

export default Input;
import type { ComponentProps } from "react";
import "./Button.css";

function Button(props: ComponentProps<"button">) {
  return <button {...props} className="button" />;
}

export default Button;

import type { ComponentProps } from "react";
import "./Button.css";

function Button({ className = "", ...props }: ComponentProps<"button">) {
  // A caller's class adds a color variant on top of the shared chunky look.
  return <button {...props} className={`button ${className}`} />;
}

export default Button;

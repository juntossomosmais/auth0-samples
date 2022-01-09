// Importing the Bootstrap CSS
import "bootstrap/dist/css/bootstrap.min.css"
// Required by React
import ReactDOM from "react-dom"
// My application
import { App } from "./App"

// In order to make React work properly
const app = document.getElementById("app")
ReactDOM.render(<App />, app)

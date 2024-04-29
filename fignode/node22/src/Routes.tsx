import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Catalog } from "./pages/Catalog";
import { Cart } from "./pages/Cart";
import '../dist/index.html'

export function AppRoutes() {
  return (
    <Router>
      <Routes>
        <Route path="/"/>
        <Route path="/cart" element={<Cart/>}/>
        <Route path="/Catalog" element={<Catalog/>}/>
        
      </Routes>
    </Router>
  )
}

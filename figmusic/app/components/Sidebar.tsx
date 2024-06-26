'use client'
import React, { useMemo } from "react";
import { usePathname } from "next/navigation";
import { BiSearch } from "react-icons/bi";
import { HiHome } from "react-icons/hi";
import Box from "./Box";
import SidebarItem from "./SidebarItem";

interface SidebarProps {
  children: React.ReactNode;
}

const Sidebar: React.FC<SidebarProps> = ({ children }) => {
  const pathname = usePathname();

  const routes = useMemo(
    () => [
      {
        icon: HiHome,
        label: "Home",
        active: pathname !== "/search",
        href: "/"
      },
      {
        icon: BiSearch,
        label: "Search",
        active: pathname === "/search",
        href: "search"
      },
    ],
    [pathname]
  );
  return (
    <div className="flex h-full">
      <div className="hidden md:flex flex-col gap-y-2 bg-black h-full w-[300px] p-2">
        <Box>
          <div className="flex flex-col px-5 py-4 gap-y-4">
            {routes.map((item) => (<SidebarItem key={item.label} {...item} />))}
          </div>
        </Box>
        <Box className="h-full overflow-y-auto">
          Song Library
        </Box>
      </div>
    </div>
  )

};
export default Sidebar;

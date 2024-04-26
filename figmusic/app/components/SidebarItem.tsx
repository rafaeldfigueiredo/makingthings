// Link is a tag built "on top" of <a>
import Link from "next/link";
import { IconType } from "react-icons";
import { twMerge } from "tailwind-merge";

// This will get the attr. stablished in Sidebar routes array
interface SidebarItemProps {
  icon: IconType;
  label: string;
  active?: boolean;
  href: string;
}

const SidebarItem: React.FC<SidebarItemProps> = (
  // Using "SIP" interface (lol)
  {
    icon:Icon,
    label,
     active,
      href
  }
) => {
  return (
    <Link 
    href={href} 
    className={twMerge(`flex flex-row h-auto items-center w-full gap-x-4 text-md font-medium cursor-pointer hover:text-white transition text-neutral-400 py-1
  `, 
  //Since the active element in the routes array isn't called with /search, the very first element rendered will be rendered with white text
  active && "text-white")}>
      <Icon size={28}/>
      <p className="truncate w-full">{label}</p>

    </Link>
  )
};

export default SidebarItem;
import {
  ChevronDownIcon,
  ChevronUpIcon,
  XMarkIcon,
} from "@heroicons/react/24/outline";
import React, { ReactChildren, ReactChild, useRef } from "react";
import Icon from "./icons";

interface IProps {
  children?: ReactChild | ReactChildren;
  title?: string | ReactChild;
  subtitle?: string | ReactChild | ReactChildren;
  count?: number;
  active?: boolean;
  cursor?: string;
  icon?: ReactChild;
  padding?: string;
  className?: string;
  open?: boolean;
  hoverable?: boolean;
}

export const SectionHeader = ({
  children,
  title,
  subtitle,
  count,
  icon,
}: IProps) => {
  return (
    <div className="mb-4">
      <h1 className="text-gray-600 text-2xl">
        {/* {count !== null && <span className="text-indigo-600 mr-1">{count}</span>} */}
        {icon && <>{icon}</>}
        {title}
        {count !== null && (
          <span className="text-indigo-600 mr-1 ml-2 text-xs">{count}</span>
        )}
      </h1>
      {subtitle && <span className="inline-block">{subtitle}</span>}
      {children}
    </div>
  );
};

export const Card = ({
  children,
  title,
  subtitle,
  hoverable = true,
  active,
  cursor = "cursor-pointer",
  padding = "p-3",
}: IProps) => {
  let border = active
    ? "border-indigo-600"
    : "border-gray-100 hover:border-indigo-600 ";
  border = hoverable ? border : "border-gray-100";

  return (
    <div
      className={`${border} border-2 bg-gray-100  group ${padding} rounded ${cursor} transition duration-300`}
    >
      <div className="mt- text-sm text-sm text-gray-500 break-words  break-words">
        {title && (
          <div className="text-indigo-700 rounded font-semibold  text-xs pb-1">
            {title}
          </div>
        )}
        <div>{subtitle}</div>
      </div>
    </div>
  );
};

export const CollapseBox = ({
  title,
  subtitle,
  children,
  className = " p-3",
  open = false,
}: IProps) => {
  const [isOpen, setIsOpen] = React.useState<boolean>(open);
  const chevronClass = "h-4 cursor-pointer inline-block mr-1";
  return (
    <div className="border border-gray-200 rounded">
      <div
        onClick={() => {
          setIsOpen(!isOpen);
        }}
        className="cursor-pointer bg-gray-100 p-2 rounded-t"
      >
        {isOpen && <ChevronUpIcon className={chevronClass} />}
        {!isOpen && <ChevronDownIcon className={chevronClass} />}

        <span className=" inline-block -mt-2 mb-2 text-xs">
          {" "}
          {/* {isOpen ? "hide" : "show"} section |  */}
          {title}
        </span>
      </div>

      {isOpen && (
        <div className={`${className} bg-gray-50  rounded`}>
          {/* <SectionHeader title={title} subtitle={subtitle} />  */}
          {children}
          {/* {!isOpen && <span> ...</span>} */}
        </div>
      )}
    </div>
  );
};

export const LoadBox = ({
  subtitle,
  className = "my-2 text-indigo-600 ",
}: IProps) => {
  return (
    <div className={`${className} `}>
      {" "}
      <span className="mr-2 ">
        {" "}
        <Icon size={5} icon="loading" />
      </span>{" "}
      {subtitle}
    </div>
  );
};

export const MessageBox = ({ title, children, className }: IProps) => {
  const messageBox = useRef(null);

  const closeMessage = () => {
    messageBox.current.remove();
  };

  return (
    <div
      ref={messageBox}
      className={`${className} p-3 bg-gray-50 rounded border border-indigo-600 transition duration-1000 ease-in-out  overflow-hidden`}
    >
      {" "}
      <div className="flex gap-2 mb-2">
        <div className="flex-1">
          {/* <span className="mr-2 text-indigo-600">
            <InformationCircleIcon className="h-6 w-6 inline-block" />
          </span>{" "} */}
          <span className="font-semibold text-gray-600 text-base">{title}</span>
        </div>
        <div>
          <span
            onClick={() => {
              closeMessage();
            }}
            className="mr-2 border cursor-pointer hover:bg-gray-100 inline-block px-1 pb-1 rounded text-gray-600"
          >
            <XMarkIcon className="h-4 w-4 inline-block" />
          </span>
        </div>
      </div>
      {children}
    </div>
  );
};

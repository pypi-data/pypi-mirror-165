import * as React from "react";
import Icon from "./icons";

const Footer = () => {
  return (
    <div className="mt-4 text-gray-500 p-3  mb-6 border-t   bg-o[pacity-90 bg-white ">
      <div>
        <span className="text-indigo-500">
          {" "}
          <Icon icon="app" size={5} />
        </span>{" "}
        Learn more about peacasso on{" "}
        <a
          target={"_blank"}
          rel={"noopener noreferrer"}
          className="underlipne inline-block border-indigo-500 border-b hover:text-indigo-500"
          href="https://github.com/victordibia/peacasso"
        >
          {" "}
          Github.
        </a>
      </div>
    </div>
  );
};
export default Footer;

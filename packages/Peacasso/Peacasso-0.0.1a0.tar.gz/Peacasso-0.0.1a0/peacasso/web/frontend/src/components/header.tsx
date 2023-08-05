import * as React from "react";
import Icon from "./icons";
import { Disclosure, Menu, Transition } from "@headlessui/react";
import { XMarkIcon, Bars3Icon, BellIcon } from "@heroicons/react/24/outline";
import { Fragment } from "react";
import { appContext } from "../hooks/provider";
import { Link } from "gatsby";

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

const Header = ({ meta, link }: any) => {
  const { user, logout } = React.useContext(appContext);
  const userName = user ? user.user.name : "Unknown";
  const userAvatarUrl = user ? user.user.avatar_url : "";
  const userID = user ? user.user.login : "unknown";

  const links = [
    { name: "Generate", href: "/" },
    // { name: "Data Explorer", href: "/explorer" },
  ];

  return (
    <Disclosure as="nav" className="bg-white mb-8 border-b border-gray-200">
      {({ open }) => (
        <>
          <div className="  px-0 sm:px-0 lg:px-0 ">
            <div className="flex justify-between h-16">
              <div className="flex  lg:px-0 ">
                <div className="flex flex-shrink-0 pt-2">
                  <a className="block  " href="/#">
                    <span className="text-indigo-600 inline-block pt-2 absolute">
                      {" "}
                      <Icon icon="app" size={10} />
                    </span>
                    <div className="pt-1 text-lg ml-14 mx-2    inline-block">
                      <div className=" flex flex-col">
                        <div>{meta.title}</div>
                        <div className="text-xs"> {meta.description}</div>
                      </div>
                    </div>
                  </a>
                </div>

                <div className="hidden md:ml-6 md:flex md:space-x-6">
                  {/* Current: "border-indigo-500 text-gray-900", Default: "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700" */}
                  {links.map((data, index) => {
                    const isActive = data.href === link;
                    const activeClass = isActive
                      ? "bg-indigo-600 "
                      : "bg-gray-100 ";
                    return (
                      <div
                        key={index + "linkrow"}
                        className={`text-gray-900 inline-flex items-center hover:text-indigo-600 hovder:bg-gray-100 px-1 pt-1 block   text-sm font-medium `}
                      >
                        <Link
                          className="hover:text-indigo-600 h-full flex flex-col"
                          to={data.href}
                        >
                          <div className=" flex-1 flex-col flex">
                            <div className="flex-1"></div>
                            <div className="pb-2 px-3">{data.name}</div>
                          </div>
                          <div
                            className={`${activeClass}  w-full h-1 rounded-t-lg `}
                          ></div>
                        </Link>
                      </div>
                    );
                  })}
                </div>
              </div>

              <div className="flex items-center md:hidden">
                {/* Mobile menu button */}
                <Disclosure.Button className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500">
                  <span className="sr-only">Open main menu</span>
                  {open ? (
                    <XMarkIcon className="block h-6 w-6" aria-hidden="true" />
                  ) : (
                    <Bars3Icon className="block h-6 w-6" aria-hidden="true" />
                  )}
                </Disclosure.Button>
              </div>
              {user && (
                <div className="hidden lg:ml-4 md:flex md:items-center">
                  <button
                    type="button"
                    className="flex-shrink-0 bg-white p-1 text-gray-400 rounded-full hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    <span className="sr-only">View notifications</span>
                    <BellIcon className="h-6 w-6" aria-hidden="true" />
                  </button>

                  <div className="ml-3">
                    <div className="text-base font-medium text-gray-800">
                      {userName}
                    </div>
                    <div className="text-xs font-normal text-gray-500">
                      {userID}
                    </div>
                  </div>

                  {/* Profile dropdown */}
                  <Menu as="div" className="ml-4 relative flex-shrink-0">
                    <div>
                      <Menu.Button className="bg-white rounded-full flex text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        <span className="sr-only">Open user menu</span>
                        <img
                          className="h-8 w-8 rounded-full"
                          src={userAvatarUrl}
                          alt=""
                        />
                      </Menu.Button>
                    </div>
                    <Transition
                      as={Fragment}
                      enter="transition ease-out duration-100"
                      enterFrom="transform opacity-0 scale-95"
                      enterTo="transform opacity-100 scale-100"
                      leave="transition ease-in duration-75"
                      leaveFrom="transform opacity-100 scale-100"
                      leaveTo="transform opacity-0 scale-95"
                    >
                      <Menu.Items className="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">
                        {/* <Menu.Item>
                        {({ active }) => (
                          <a
                            href="#"
                            className={classNames(active ? 'bg-gray-100' : '', 'block px-4 py-2 text-sm text-gray-700')}
                          >
                            Your Profile
                          </a>
                        )}
                      </Menu.Item> */}

                        <Menu.Item>
                          {({ active }) => (
                            <a
                              href="#"
                              onClick={() => {
                                logout();
                              }}
                              className={classNames(
                                active ? "bg-gray-100" : "",
                                "block px-4 py-2 text-sm text-gray-700"
                              )}
                            >
                              Sign out
                            </a>
                          )}
                        </Menu.Item>
                      </Menu.Items>
                    </Transition>
                  </Menu>
                </div>
              )}
            </div>
          </div>

          <Disclosure.Panel className="md:hidden">
            <div className="pt-2 pb-3 space-y-1">
              {/* Current: "bg-indigo-50 border-indigo-500 text-indigo-700", Default: "border-transparent text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800" */}
              {links.map((data, index) => {
                return (
                  <Disclosure.Button
                    key={index + "linkrow"}
                    as="a"
                    href={data.href}
                    className="bg-indigo-50 border-indigo-500 text-indigo-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
                  >
                    {data.name}
                  </Disclosure.Button>
                );
              })}
            </div>
            {user && (
              <div className="pt-4 pb-3 border-t border-gray-200">
                <div className="flex items-center px-4">
                  <div className="flex-shrink-0">
                    <img
                      className="h-10 w-10 rounded-full"
                      src={userAvatarUrl}
                      alt=""
                    />
                  </div>
                  <div className="ml-3">
                    <div className="text-base font-medium text-gray-800">
                      {userName}
                    </div>
                    <div className="text-sm font-medium text-gray-500">
                      {userID}
                    </div>
                  </div>
                  <button
                    type="button"
                    className="ml-auto flex-shrink-0 bg-white p-1 text-gray-400 rounded-full hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    <span className="sr-only">View notifications</span>
                    <BellIcon className="h-6 w-6" aria-hidden="true" />
                  </button>
                </div>
                <div className="mt-3 space-y-1">
                  {/* <Disclosure.Button
                  as="a"
                  href="#"
                  className="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
                >
                  Your Profile
                </Disclosure.Button> */}
                  {/* <Disclosure.Button
                  as="a"
                  href="#"
                  className="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
                >
                  Settings
                </Disclosure.Button> */}
                  <Disclosure.Button
                    as="a"
                    href="#"
                    onClick={() => logout()}
                    className="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
                  >
                    Sign out
                  </Disclosure.Button>
                </div>
              </div>
            )}
          </Disclosure.Panel>
        </>
      )}
    </Disclosure>
  );
};

export default Header;

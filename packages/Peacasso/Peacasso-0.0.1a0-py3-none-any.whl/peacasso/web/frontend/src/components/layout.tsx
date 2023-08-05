import * as React from "react";
import Header from "./header";
import { appContext } from "../hooks/provider";
import LoginView from "./login";
import Footer from "./footer";
import { graphql } from "gatsby";

type Props = {
  title: string;
  link: string;
  children?: React.ReactNode;
  showHeader?: boolean;
  restricted?: boolean;
  meta?: any;
};

const Layout = ({
  meta,
  title,
  link,
  children,
  showHeader = true,
  restricted = false,
}: Props) => {
  const LayoutView = () => {
    return (
      <div style={{ height: "100%" }} className="  flex flex-col   ">
        <div className="flex-1">
          <title>{meta?.title + " | " + title}</title>
          {showHeader && <Header meta={meta} link={link} />}
          <div>{children}</div>
        </div>
        <Footer />
      </div>
    );
  };
  return (
    <appContext.Consumer>
      {(context: { user: any }) => {
        // console.log("context", context);
        if (restricted) {
          return (
            <div className="h-screen ">
              {context.user && <LayoutView />}
              {!context.user && <LoginView meta={meta} />}
            </div>
          );
        } else {
          return <LayoutView />;
        }
      }}
    </appContext.Consumer>
  );
};

export default Layout;

import React from 'react';
import styles from './ClassDiagram.css';
import classnames from 'classnames';
import { Pane, Popover } from 'evergreen-ui';

const cx = args => classnames(styles, args)

export const generateFunctionText = funcData => {
    return Object.keys(funcData).map(func => {
        const args = funcData[func].arguments;
        const ret = funcData[func].returnType;
        return `+ ${func}(${Object.keys(args).map(arg => `${arg} : ${args[arg]}`)}) : ${ret}`;
    })
}

export const generateClassArgsText = classArgs => {
    return Object.keys(classArgs).map(arg => <p>{`+ ${arg} : ${classArgs[arg]}`}</p>)
}

function ClassDiagram(node) {
    const {
        id,
        classParent,
        classArgs,
        classFunctions,
    } = node.data;

    return (
        <Popover
            content={
                <Pane
                    width={400}
                    height={200}
                    display="flex"
                    alignItems="center"
                    justifyContent="center"
                    flexDirection="column"
                    >
                    <div className={cx('classDiagramTable')} id="box">
                        <div className={cx('className')}>{ id }</div>
                        <div className={cx('hrLine')}><hr/></div>
                        <div className={cx('classParent')}>Inherits from: { classParent }</div>
                        <div className={cx('hrLine')}><hr/></div>
                        <div className={cx('classArgs')}>{ generateClassArgsText(classArgs) }</div>
                        <div className={cx('hrLine')}><hr/></div>
                        <div className={cx('classFunctions')}>{ generateFunctionText(classFunctions) }</div>
                    </div>
                </Pane>
            }>
                <Pane
                    width={50}
                    height={50}
                    display="flex"
                    alignItems="center"
                    justifyContent="center"
                    backgroundColor="green"
                    >
                        { id }
                </Pane>
            </Popover>
    )
};

export default ClassDiagram;

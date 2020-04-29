import React from 'react';
import styles from './ClassDiagram.css';
import classnames from 'classnames';

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

const ClassDiagram = props => {
    const className = "ClassTest";
    const classParent = ['A', 'B', 'C'];
    const classArgs = {"Arg1": "String", "Arg2": "Int"}
    const classFunctions = {
        "Function1": {
            arguments: {
                "Arg1": "String",
                "Arg2": "Int",
            },
            returnType: "String"
    }};

    return (
        <div className={cx('classDiagramTable')} id="box">
            <div className={cx('className')}>{ className }</div>
            <div className={cx('hrLine')}><hr/></div>
            <div className={cx('classParent')}>Inherits from: { classParent }</div>
            <div className={cx('hrLine')}><hr/></div>
            <div className={cx('classArgs')}>{ generateClassArgsText(classArgs) }</div>
            <div className={cx('hrLine')}><hr/></div>
            <div className={cx('classFunctions')}>{ generateFunctionText(classFunctions) }</div>
        </div>
    )
};

export default ClassDiagram;

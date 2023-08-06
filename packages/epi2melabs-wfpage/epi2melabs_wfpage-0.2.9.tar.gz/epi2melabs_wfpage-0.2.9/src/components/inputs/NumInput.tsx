import React from 'react';
import styled from 'styled-components';
import StyledTooltip from '../common/Tooltip';

// -----------------------------------------------------------------------------
// Type definitions
// -----------------------------------------------------------------------------
export const NUM_INPUT = 'number';
export const INT_INPUT = 'integer';

export interface INumProps {
  id: string;
  label: string;
  format: string;
  description?: string;
  help_text?: string;
  defaultValue?: number;
  min: number;
  max: number;
}

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface INumInput extends INumProps {
  error: string[];
  onChange: CallableFunction;
  className?: string;
}

const NumInput = ({
  id,
  label,
  format,
  description,
  help_text,
  defaultValue,
  min,
  max,
  error,
  onChange,
  className
}: INumInput): JSX.Element => (
  <div className={`num-input ${className}`}>
    <div className="num-input-header">
      <div>
        <h4>{label}</h4>
        {description ? <p>{description}</p> : ''}
      </div>
      {help_text ? (
        <div className="num-input-help">
          <StyledTooltip text={help_text} />
        </div>
      ) : (
        ''
      )}
    </div>
    <label htmlFor={id}>
      <input
        id={id}
        type="number"
        defaultValue={defaultValue}
        min={min}
        max={max}
        onChange={(e: any) => onChange(id, Number(e.target.value))}
      />
    </label>
    {error.length ? (
      <div className="error">
        {error.map(Error => (
          <p>Error: {Error}</p>
        ))}
      </div>
    ) : (
      ''
    )}
  </div>
);

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledNumInput = styled(NumInput)`
  h4 {
    padding: 0 0 5px 0;
  }

  p {
    padding: 0 0 10px 0;
  }

  label {
    display: flex;
  }

  input {
    margin: 0;
    padding: 15px 25px;

    font-size: 14px;
    line-height: 1em;

    color: #212529;
    background-color: #f8f9fa;
    border: 1px solid rgba(0, 0, 0, 0.125);
    border-radius: 4px;
    outline: none;

    transition: 0.2s ease-in-out all;
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }

  input:hover {
    border-color: #005c75;
    box-shadow: 0 0 0 0.25rem rgb(13 110 253 / 25%);
  }

  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
  }

  .num-input-header {
    display: flex;
    justify-content: space-between;
  }

  .num-input-help {
    position: relative;
    cursor: pointer;
    display: flex;
    align-items: flex-end;
    padding: 0 0 10px 0;
  }
`;

export default StyledNumInput;

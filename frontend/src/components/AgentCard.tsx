import React from 'react';
import type { Agent } from '../types/models';

export interface AgentCardProps {
  /** The agent data to display */
  agent: Agent;
  /** Callback fired when the "Contact Agent" button is clicked */
  onContact: (agent: Agent) => void;
  /** Layout orientation: vertical (sidebar) or horizontal */
  layout?: 'vertical' | 'horizontal';
  /** Optional additional CSS class names */
  className?: string;
}

const AgentCard: React.FC<AgentCardProps> = ({
  agent,
  onContact,
  layout = 'vertical',
  className = '',
}) => {
  const handleContact = () => {
    onContact(agent);
  };

  if (layout === 'horizontal') {
    return (
      <div
        data-testid="agent-card"
        className={`bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 p-6 flex flex-row items-center gap-6 ${className}`}
      >
        <div className="flex-shrink-0">
          <img
            src={agent.photo}
            alt={`${agent.name} headshot`}
            className="w-24 h-24 rounded-full object-cover ring-2 ring-blue-100"
          />
        </div>

        <div className="flex-1 min-w-0">
          <h3 className="text-xl font-bold text-gray-900 truncate">
            {agent.name}
          </h3>
          <p className="text-sm font-medium text-blue-600 mt-0.5">
            {agent.title}
          </p>
          <p className="text-sm text-gray-600 mt-2 line-clamp-2">
            {agent.bio}
          </p>
          <div className="flex flex-wrap items-center gap-4 mt-3 text-sm text-gray-500">
            <a
              href={`tel:${agent.phone}`}
              className="hover:text-blue-600 transition-colors flex items-center gap-1"
              data-testid="agent-phone"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              {agent.phone}
            </a>
            <a
              href={`mailto:${agent.email}`}
              className="hover:text-blue-600 transition-colors flex items-center gap-1 truncate"
              data-testid="agent-email"
            >
              <svg className="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <span className="truncate">{agent.email}</span>
            </a>
          </div>
        </div>

        <div className="flex-shrink-0">
          <button
            onClick={handleContact}
            data-testid="contact-button"
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 px-6 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 whitespace-nowrap"
          >
            Contact Agent
          </button>
        </div>
      </div>
    );
  }

  return (
    <div
      data-testid="agent-card"
      className={`bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 p-6 text-center ${className}`}
    >
      <div className="flex justify-center mb-4">
        <img
          src={agent.photo}
          alt={`${agent.name} headshot`}
          className="w-28 h-28 rounded-full object-cover ring-4 ring-blue-50"
        />
      </div>

      <h3 className="text-xl font-bold text-gray-900">{agent.name}</h3>
      <p className="text-sm font-medium text-blue-600 mt-1">{agent.title}</p>

      <div className="mt-4 space-y-1.5 text-sm text-gray-500">
        <a
          href={`tel:${agent.phone}`}
          className="flex items-center justify-center gap-2 hover:text-blue-600 transition-colors"
          data-testid="agent-phone"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
          </svg>
          {agent.phone}
        </a>
        <a
          href={`mailto:${agent.email}`}
          className="flex items-center justify-center gap-2 hover:text-blue-600 transition-colors"
          data-testid="agent-email"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
          {agent.email}
        </a>
      </div>

      <p className="text-sm text-gray-600 mt-4 leading-relaxed line-clamp-3">
        {agent.bio}
      </p>

      <button
        onClick={handleContact}
        data-testid="contact-button"
        className="mt-5 w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 px-6 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      >
        Contact Agent
      </button>
    </div>
  );
};

export default AgentCard;

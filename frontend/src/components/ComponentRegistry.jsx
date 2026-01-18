import React from 'react';

// ============================================
// NAVIGATION COMPONENTS
// ============================================

const NavbarComponent = ({ logo, links }) => (
    <div className="navbar" style={{
        width: '100%',
        height: '100%',
        backgroundColor: '#94a3b8',
        padding: '0.75rem 1.5rem',
        color: 'black'
    }}>
        <div className="flex-1">
            <a className="btn btn-ghost normal-case text-xl font-bold hover:bg-black/10" style={{ color: '#000000' }}>
                {logo || 'Brand'}
            </a>
        </div>
        <div className="flex-none">
            <ul className="menu menu-horizontal px-1 gap-1">
                {(links && Array.isArray(links) ? links : ['Home', 'About', 'Contact']).map((link, i) => (
                    <li key={i}><a className="hover:bg-black/10 rounded-lg" style={{ color: '#000000' }}>{link}</a></li>
                ))}
            </ul>
        </div>
    </div>
);

const NavbarWithDropdown = () => (
    <div className="navbar" style={{
        width: '100%',
        height: '100%',
        backgroundColor: '#94a3b8',
        padding: '0.75rem 1.5rem',
        color: 'black'
    }}>
        <div className="flex-1">
            <a className="btn btn-ghost normal-case text-xl font-bold hover:bg-black/10" style={{ color: '#000000' }}>
                Brand
            </a>
        </div>
        <div className="flex-none">
            <ul className="menu menu-horizontal px-1 gap-1">
                <li><a className="hover:bg-black/10 rounded-lg" style={{ color: '#000000' }}>Home</a></li>
                <li>
                    <details>
                        <summary className="hover:bg-black/10 rounded-lg" style={{ color: '#000000' }}>Menu</summary>
                        <ul className="p-2 shadow-lg bg-white rounded-lg mt-2" style={{ minWidth: '150px' }}>
                            <li><a className="hover:bg-slate-100 rounded-lg" style={{ color: '#000000' }}>Submenu 1</a></li>
                            <li><a className="hover:bg-slate-100 rounded-lg" style={{ color: '#000000' }}>Submenu 2</a></li>
                        </ul>
                    </details>
                </li>
                <li><a className="hover:bg-black/10 rounded-lg" style={{ color: '#000000' }}>Contact</a></li>
            </ul>
        </div>
    </div>
);

const BreadcrumbsComponent = () => (
    <div className="text-sm breadcrumbs p-4" style={{ width: '100%', height: '100%' }}>
        <ul>
            <li><a>Home</a></li>
            <li><a>Documents</a></li>
            <li>Add Document</li>
        </ul>
    </div>
);

const TabsComponent = () => (
    <div className="tabs tabs-boxed p-4" style={{ width: '100%', height: '100%' }}>
        <a className="tab tab-active">Tab 1</a>
        <a className="tab">Tab 2</a>
        <a className="tab">Tab 3</a>
    </div>
);

// ============================================
// BUTTON COMPONENTS
// ============================================

const ButtonPrimary = () => (
    <button className="btn btn-primary w-full h-full">Primary Button</button>
);

const ButtonSecondary = () => (
    <button className="btn btn-secondary w-full h-full">Secondary Button</button>
);

const ButtonAccent = () => (
    <button className="btn btn-accent w-full h-full">Accent Button</button>
);

const ButtonGroup = () => (
    <div className="p-4 w-full h-full">
        <div className="btn-group w-full h-full">
            <button className="btn flex-1 h-full">Button 1</button>
            <button className="btn btn-active flex-1 h-full">Button 2</button>
            <button className="btn flex-1 h-full">Button 3</button>
        </div>
    </div>
);

const ButtonOutline = () => (
    <button className="btn btn-outline btn-primary w-full h-full">Outline Button</button>
);

// ============================================
// CARD COMPONENTS
// ============================================

const CardBasic = ({ title, content }) => (
    <div className="card bg-slate-300 shadow-xl text-black" style={{ width: '100%', height: '100%' }}>
        <div className="card-body p-8">
            <h2 className="card-title">{title || 'Card Title'}</h2>
            <p>{content || 'A card component with a shadow and padding.'}</p>
            <div className="card-actions justify-end">
                <button className="btn btn-primary">Action</button>
            </div>
        </div>
    </div>
);

const CardWithImage = () => (
    <div className="card bg-slate-300 shadow-xl text-black" style={{ width: '100%', height: '100%' }}>
        <figure>
            <div className="bg-gray-200 w-full h-[60px] flex items-center justify-center text-gray-500 text-sm">
                [image of shoes]
            </div>
        </figure>
        <div className="card-body p-8">
            <h2 className="card-title">Shoes!</h2>
            <p>If a dog chews shoes whose shoes does he choose?</p>
            <div className="card-actions justify-end">
                <button className="btn btn-primary">Buy Now</button>
            </div>
        </div>
    </div>
);

const CardCompact = () => (
    <div className="card card-compact bg-slate-300 shadow-xl text-black" style={{ width: '100%', height: '100%' }}>
        <div className="card-body p-8">
            <h2 className="card-title">Compact Card</h2>
            <p>This card has less padding for tighter spaces.</p>
            <div className="card-actions justify-end">
                <button className="btn btn-primary btn-sm">Small Button</button>
            </div>
        </div>
    </div>
);

// ============================================
// FORM COMPONENTS
// ============================================

const InputText = () => (
    <div className="p-4" style={{ width: '100%', height: '100%' }}>
        <input type="text" placeholder="Type here" className="input input-bordered w-full h-full" />
    </div>
);

const InputWithLabel = () => (
    <div className="form-control p-4" style={{ width: '100%', height: '100%' }}>
        <label className="label">
            <span className="label-text text-black">What is your name?</span>
        </label>
        <input type="text" placeholder="Type here" className="input input-bordered w-full h-full" />
    </div>
);

const TextareaComponent = () => (
    <div className="p-4" style={{ width: '100%', height: '100%' }}>
        <textarea className="textarea textarea-bordered w-full h-full" placeholder="Bio" rows="4"></textarea>
    </div>
);

const SelectComponent = () => (
    <div className="p-4" style={{ width: '100%', height: '100%' }}>
        <select className="select select-bordered w-full h-full">
            <option disabled selected>Pick one</option>
            <option>Option 1</option>
            <option>Option 2</option>
            <option>Option 3</option>
        </select>
    </div>
);

const CheckboxComponent = () => (
    <div className="form-control p-4" style={{ width: '100%' }}>
        <label className="label cursor-pointer justify-start gap-2">
            <input type="checkbox" defaultChecked className="checkbox checkbox-success" />
            <span className="label-text">Remember me</span>
        </label>
    </div>
);

const RadioGroup = () => (
    <div className="form-control p-4" style={{ width: '100%' }}>
        <label className="label cursor-pointer justify-start gap-2">
            <input type="radio" name="radio-10" className="radio" defaultChecked />
            <span className="label-text">Option 1</span>
        </label>
        <label className="label cursor-pointer justify-start gap-2">
            <input type="radio" name="radio-10" className="radio" />
            <span className="label-text">Option 2</span>
        </label>
    </div>
);

const RangeSlider = () => (
    <div className="p-4" style={{ width: '100%', display: 'flex', alignItems: 'center', maxHeight: '40px' }}>
        <input
            type="range"
            min={0}
            max="100"
            defaultValue="40"
            className="range range-sm w-full"
            style={{
                accentColor: '#4b5563',
                height: '6px',
                maxHeight: '6px'
            }}
        />
    </div>
);

const ToggleSwitch = () => (
    <div className="form-control p-4" style={{ width: '100%' }}>
        <label className="label cursor-pointer justify-start gap-2">
            <input type="checkbox" className="toggle toggle-accent" defaultChecked />
            <span className="label-text text-black">Toggle</span>
        </label>
    </div>
);

// ============================================
// DISPLAY COMPONENTS
// ============================================

const AlertInfo = () => (
    <div className="p-4 w-full h-full">
        <div className="alert alert-info shadow-lg h-full">
            <div style={{ height: '100%', display: 'flex', alignItems: 'center' }}>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" className="stroke-current flex-shrink-0 w-6 h-6"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span>New software update available.</span>
            </div>
        </div>
    </div>
);

const AlertSuccess = () => (
    <div className="p-4 w-full h-full">
        <div className="alert alert-success shadow-lg h-full">
            <div style={{ height: '100%', display: 'flex', alignItems: 'center' }}>
                <svg xmlns="http://www.w3.org/2000/svg" className="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>Your purchase has been confirmed!</span>
            </div>
        </div>
    </div>
);

const BadgeComponent = () => (
    <div className="w-full h-full flex justify-center items-center p-4">
        <div className="badge badge-primary">Badge</div>
    </div>
);

const BadgeGroup = () => (
    <div className="flex gap-2 w-full h-full justify-center items-center p-4">
        <div className="badge badge-primary">Primary</div>
        <div className="badge badge-secondary">Secondary</div>
        <div className="badge badge-accent">Accent</div>
    </div>
);

const ProgressBar = () => (
    <div className="p-4" style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center' }}>
        <progress className="progress progress-primary w-full" value="70" max="100"></progress>
    </div>
);

const RadialProgress = () => (
    <div className="w-full h-full flex justify-center items-center p-4">
        <div className="radial-progress text-primary" style={{ "--value": 70 }} role="progressbar">70%</div>
    </div>
);

const StatsComponent = ({ stats }) => (
    <div className="stats shadow w-full h-full">
        {(stats && Array.isArray(stats) ? stats : [
            { label: 'Downloads', value: '31K', desc: 'Jan 1st - Feb 1st' },
            { label: 'New Users', value: '4,200', desc: '↗︎ 40 (2%)' }
        ]).map((stat, i) => (
            <div key={i} className="stat place-items-center">
                <div className="stat-title">{stat.label}</div>
                <div className="stat-value text-primary">{stat.value}</div>
                <div className="stat-desc text-primary">{stat.desc}</div>
            </div>
        ))}
    </div>
);

const CalendarComponent = () => (
    <div className="card bg-base-100 shadow-xl w-full h-full overflow-hidden flex flex-col items-center justify-center p-6">
        <div className="flex justify-between w-full mb-4 px-2">
            <button className="btn btn-sm btn-ghost">❮</button>
            <span className="font-bold text-lg">October 2024</span>
            <button className="btn btn-sm btn-ghost">❯</button>
        </div>
        <div className="grid grid-cols-7 gap-2 text-center w-full">
            <div className="text-xs font-bold opacity-50">Su</div>
            <div className="text-xs font-bold opacity-50">Mo</div>
            <div className="text-xs font-bold opacity-50">Tu</div>
            <div className="text-xs font-bold opacity-50">We</div>
            <div className="text-xs font-bold opacity-50">Th</div>
            <div className="text-xs font-bold opacity-50">Fr</div>
            <div className="text-xs font-bold opacity-50">Sa</div>
            {[...Array(35)].map((_, i) => {
                const day = i - 2;
                if (day < 1 || day > 31) return <div key={i}></div>;
                return (
                    <div key={i} className={`p-2 rounded-lg hover:bg-base-200 cursor-pointer text-sm ${day === 15 ? 'bg-primary text-primary-content font-bold' : ''}`}>
                        {day}
                    </div>
                );
            })}
        </div>
    </div>
);

const PricingComponent = ({ plans }) => (
    <div className="w-full h-full flex flex-row gap-6 justify-center items-center bg-base-200 p-6 overflow-x-auto">
        {(plans && Array.isArray(plans) ? plans : [
            { name: 'Basic', price: '$0', desc: 'Free forever' },
            { name: 'Pro', price: '$29', desc: 'Best for small teams' }
        ]).map((plan, i) => (
            <div key={i} className="card bg-base-100 w-60 flex-shrink-0 shadow-lg h-full">
                <div className="card-body items-center text-center p-6">
                    <h2 className="card-title">{plan.name}</h2>
                    <div className="text-4xl font-bold py-4">{plan.price}</div>
                    <div className="text-sm opacity-70">{plan.desc || plan.features?.join(', ')}</div>
                    <div className="card-actions mt-auto w-full">
                        <button className="btn btn-outline btn-primary w-full">Get Started</button>
                    </div>
                </div>
            </div>
        ))}
    </div>
);

// ============================================
// HERO SECTIONS
// ============================================

const HeroBasic = ({ headline, subheadline, cta }) => (
    <div className="hero bg-base-200 p-4" style={{ width: '100%', height: '100%' }}>
        <div className="hero-content text-center">
            <div className="max-w-md">
                <h1 className="text-5xl font-bold">{headline || 'Hello there'}</h1>
                <p className="py-6">{subheadline || 'Provident cupiditate voluptatem et in. Quaerat fugiat ut assumenda excepturi exercitationem quasi.'}</p>
                <button className="btn btn-primary">{cta || 'Get Started'}</button>
            </div>
        </div>
    </div>
);

const HeroWithImage = ({ headline, content, cta }) => (
    <div className="hero bg-base-200 p-4" style={{ width: '100%', height: '100%' }}>
        <div className="hero-content flex-row gap-8">
            <div className="w-48 h-48 bg-base-300 flex items-center justify-center shadow-lg flex-shrink-0">Image</div>
            <div>
                <h1 className="text-3xl font-bold">{headline || 'Content Section'}</h1>
                <p className="py-4">{content || 'Add your content description here.'}</p>
                <button className="btn btn-primary">{cta || 'Learn More'}</button>
            </div>
        </div>
    </div>
);

// ============================================
// MODAL & OVERLAY COMPONENTS
// ============================================

const ModalComponent = () => (
    <div className="mockup-window border border-base-300 bg-base-200" style={{ width: '100%', height: '100%' }}>
        <div className="px-4 py-16 bg-base-200">
            <p className="text-center">Modal Content Here</p>
            <div className="modal-action justify-center">
                <button className="btn">Close</button>
            </div>
        </div>
    </div>
);

const DrawerComponent = () => (
    <div className="bg-base-100 p-4 rounded-lg border border-base-300" style={{ width: '100%', height: '100%' }}>
        <div className="flex flex-col gap-3">
            <button className="btn btn-primary">Open Drawer</button>
            <div className="text-sm text-base-content opacity-60">
                Interactive drawer component
            </div>
        </div>
    </div>
);

// ============================================
// DROPDOWN COMPONENTS
// ============================================

const DropdownBasic = () => (
    <div className="p-4 w-full h-full">
        <div className="dropdown w-full h-full">
            <label tabIndex={0} className="btn m-1 w-full h-full">Click</label>
            <ul tabIndex={0} className="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
                <li><a>Item 1</a></li>
                <li><a>Item 2</a></li>
                <li><a>Item 3</a></li>
            </ul>
        </div>
    </div>
);

const DropdownHover = () => (
    <div className="p-4 w-full h-full">
        <div className="dropdown dropdown-hover w-full h-full">
            <label tabIndex={0} className="btn m-1 w-full h-full">Hover</label>
            <ul tabIndex={0} className="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
                <li><a>Item 1</a></li>
                <li><a>Item 2</a></li>
            </ul>
        </div>
    </div>
);

// ============================================
// DEVICE FRAME COMPONENTS
// ============================================

const MacBookFrame = ({ device }) => (
    <div style={{
        width: '100%',
        height: '100%',
        backgroundColor: '#1e293b',
        borderRadius: '12px',
        border: '3px solid #334155',
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
        position: 'relative',
        overflow: 'hidden'
    }}>
        {/* Browser chrome / top bar */}
        <div style={{
            height: '28px',
            backgroundColor: '#334155',
            display: 'flex',
            alignItems: 'center',
            paddingLeft: '12px',
            gap: '6px'
        }}>
            <div style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#ef4444' }}></div>
            <div style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#eab308' }}></div>
            <div style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: '#22c55e' }}></div>
        </div>
        {/* Screen area - content renders on top */}
        <div style={{
            width: '100%',
            height: 'calc(100% - 28px)',
            backgroundColor: '#0f172a'
        }}>
        </div>
    </div>
);

// ============================================
// FOOTER COMPONENTS
// ============================================

const FooterBasic = () => (
    <footer className="footer p-10 bg-base-200 text-base-content" style={{ width: '100%', height: '100%' }}>
        <nav>
            <header className="footer-title">Services</header>
            <a className="link link-hover">Branding</a>
            <a className="link link-hover">Design</a>
            <a className="link link-hover">Marketing</a>
        </nav>
        <nav>
            <header className="footer-title">Company</header>
            <a className="link link-hover">About us</a>
            <a className="link link-hover">Contact</a>
            <a className="link link-hover">Jobs</a>
        </nav>
        <nav>
            <header className="footer-title">Legal</header>
            <a className="link link-hover">Terms of use</a>
            <a className="link link-hover">Privacy policy</a>
            <a className="link link-hover">Cookie policy</a>
        </nav>
    </footer>
);

const FooterCentered = () => (
    <footer className="footer footer-center p-10 bg-base-200 text-base-content" style={{ width: '100%', height: '100%' }}>
        <nav className="grid grid-flow-col gap-4">
            <a className="link link-hover">About us</a>
            <a className="link link-hover">Contact</a>
            <a className="link link-hover">Jobs</a>
            <a className="link link-hover">Press kit</a>
        </nav>
        <aside>
            <p>Copyright © 2024 - All right reserved</p>
        </aside>
    </footer>
);

// ============================================
// COMPONENT REGISTRY
// ============================================

export const COMPONENT_REGISTRY = {
    // Navigation
    'navbar': NavbarComponent,
    'navbar-dropdown': NavbarWithDropdown,
    'breadcrumbs': BreadcrumbsComponent,
    'tabs': TabsComponent,

    // Buttons
    'button-primary': ButtonPrimary,
    'button-secondary': ButtonSecondary,
    'button-accent': ButtonAccent,
    'button-group': ButtonGroup,
    'button-outline': ButtonOutline,

    // Cards
    'card-basic': CardBasic,
    'card-image': CardWithImage,
    'card-compact': CardCompact,

    // Forms
    'input-text': InputText,
    'input-label': InputWithLabel,
    'textarea': TextareaComponent,
    'select': SelectComponent,
    'checkbox': CheckboxComponent,
    'radio': RadioGroup,
    'range': RangeSlider,
    'toggle': ToggleSwitch,

    // Display
    'alert-info': AlertInfo,
    'alert-success': AlertSuccess,
    'badge': BadgeComponent,
    'badge-group': BadgeGroup,
    'progress': ProgressBar,
    'radial-progress': RadialProgress,
    'progress': ProgressBar,
    'radial-progress': RadialProgress,
    'stats': StatsComponent,
    'calendar': CalendarComponent,
    'pricing': PricingComponent,

    // Hero
    'hero-basic': HeroBasic,
    'hero-image': HeroWithImage,

    // Modal & Overlay
    'modal': ModalComponent,
    'drawer': DrawerComponent,

    // Dropdown
    'dropdown': DropdownBasic,
    'dropdown-hover': DropdownHover,

    // Footer
    'footer-basic': FooterBasic,
    'footer-centered': FooterCentered,

    // Standard Generalized Types (UPPERCASE - Backend sync)
    'NAVIGATION-BAR': NavbarComponent,
    'HERO-BANNER': HeroBasic,
    'SECTION': CardBasic,
    'CARD': CardBasic,
    'CONTENT-BLOCK': HeroWithImage,
    'FEATURE-GRID': PricingComponent, // Can use pricing as grid for now
    'PRICING-TABLE': PricingComponent,
    'FOOTER-SIMPLE': FooterBasic,
    'SIDEBAR': DrawerComponent,
    'BOTTOM_NAV': TabsComponent,
    'FORM': InputWithLabel,
    'BUTTON': ButtonPrimary,
    'INPUT': InputText,
    'TEXT': TextareaComponent,
    'HEADING': HeroBasic,
    'IMAGE': CardWithImage,
    'TABLE': StatsComponent,
    'CALENDAR': CalendarComponent,
    'CHART': RadialProgress,
    'FRAME': MacBookFrame,

    // Backend compatible types
    'NAVBAR': NavbarComponent,
    'HERO': HeroBasic,
    'FOOTER': FooterBasic,
};

export const getComponentByType = (type) => {
    if (!type) return null;
    const normalizedType = type.toLowerCase();

    return COMPONENT_REGISTRY[type] ||
        COMPONENT_REGISTRY[normalizedType] ||
        COMPONENT_REGISTRY[type.toUpperCase()] ||
        COMPONENT_REGISTRY[type.replace(/-/g, '_').toUpperCase()] ||
        null;
};

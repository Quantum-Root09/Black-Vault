#!/usr/bin/env python3
"""
Professional Domain Lookup Tool with GUI
Features: Multiple WHOIS databases, DNSSEC, Registrant Info, etc.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import whois
import dns.resolver
import requests
import json
from datetime import datetime
import threading
import re
from typing import Dict, Optional

class DomainLookupGUI:
    """Main GUI Application for Domain Lookup"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Domain Lookup Tool v2.0")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # Set custom fonts
        self.title_font = font.Font(family="Segoe UI", size=16, weight="bold")
        self.header_font = font.Font(family="Segoe UI", size=12, weight="bold")
        self.text_font = font.Font(family="Consolas", size=10)
        
        # Available WHOIS providers
        self.providers = {
            "1": {
                "name": "Standard WHOIS Database",
                "description": "Official WHOIS database via python-whois",
                "method": self.lookup_standard_whois
            },
            "2": {
                "name": "WhoisXML API",
                "description": "Comprehensive WHOIS data with API",
                "method": self.lookup_whoisxml
            },
            "3": {
                "name": "IPInfo WHOIS",
                "description": "Alternative WHOIS database",
                "method": self.lookup_ipinfo
            },
            "4": {
                "name": "SecurityTrails",
                "description": "Historical WHOIS data",
                "method": self.lookup_securitytrails
            }
        }
        
        self.current_result = None
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the main GUI interface"""
        
        # Main container
        main_container = tk.Frame(self.root, bg='#1e1e1e')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header Section
        header_frame = tk.Frame(main_container, bg='#2d2d2d', height=100)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🔍 PROFESSIONAL DOMAIN LOOKUP TOOL", 
                               font=self.title_font, bg='#2d2d2d', fg='#00ff00')
        title_label.pack(pady=20)
        
        # Search Section
        search_frame = tk.Frame(main_container, bg='#2d2d2d', height=80)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        search_frame.pack_propagate(False)
        
        tk.Label(search_frame, text="Enter Domain Name:", font=self.header_font, 
                bg='#2d2d2d', fg='#ffffff').pack(side=tk.LEFT, padx=10)
        
        self.domain_entry = tk.Entry(search_frame, font=("Segoe UI", 12), width=40,
                                     bg='#3c3c3c', fg='#ffffff', insertbackground='white')
        self.domain_entry.pack(side=tk.LEFT, padx=10)
        self.domain_entry.bind('<Return>', lambda e: self.search_domain())
        
        self.search_button = tk.Button(search_frame, text="🔍 SEARCH DOMAIN", 
                                       command=self.search_domain,
                                       bg='#007acc', fg='white', font=self.header_font,
                                       padx=20, pady=5, cursor="hand2")
        self.search_button.pack(side=tk.LEFT, padx=10)
        
        # Progress Bar
        self.progress = ttk.Progressbar(search_frame, mode='indeterminate', length=200)
        self.progress.pack(side=tk.LEFT, padx=10)
        self.progress.pack_forget()
        
        # Provider Selection Section
        provider_frame = tk.LabelFrame(main_container, text="Select WHOIS Database Provider", 
                                       font=self.header_font, bg='#2d2d2d', fg='#00ff00',
                                       padx=10, pady=10)
        provider_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.provider_var = tk.StringVar(value="1")
        
        for key, provider in self.providers.items():
            rb = tk.Radiobutton(provider_frame, text=f"{provider['name']} - {provider['description']}",
                               variable=self.provider_var, value=key,
                               bg='#2d2d2d', fg='#ffffff', selectcolor='#2d2d2d',
                               activebackground='#2d2d2d', activeforeground='#00ff00')
            rb.pack(anchor=tk.W, pady=2)
        
        # Results Section with Notebook (Tabs)
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Domain Information
        self.domain_info_frame = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(self.domain_info_frame, text="📋 Domain Information")
        self.setup_domain_info_tab()
        
        # Tab 2: Registrant Contact
        self.registrant_frame = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(self.registrant_frame, text="👤 Registrant Contact")
        self.setup_contact_tab(self.registrant_frame, "Registrant")
        
        # Tab 3: Technical Contact
        self.technical_frame = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(self.technical_frame, text="🔧 Technical Contact")
        self.setup_contact_tab(self.technical_frame, "Technical")
        
        # Tab 4: Administrative Contact
        self.admin_frame = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(self.admin_frame, text="👔 Administrative Contact")
        self.setup_contact_tab(self.admin_frame, "Administrative")
        
        # Tab 5: Registrar Information
        self.registrar_frame = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(self.registrar_frame, text="🏢 Registrar Information")
        self.setup_registrar_tab()
        
        # Tab 6: DNSSEC & Security
        self.security_frame = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(self.security_frame, text="🔒 DNSSEC & Security")
        self.setup_security_tab()
        
        # Tab 7: Raw WHOIS Data
        self.raw_frame = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(self.raw_frame, text="📄 Raw WHOIS Data")
        self.setup_raw_tab()
        
        # Status Bar
        self.status_bar = tk.Label(main_container, text="Ready", bd=1, relief=tk.SUNKEN,
                                   anchor=tk.W, bg='#2d2d2d', fg='#00ff00')
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Back to Menu Button
        back_button = tk.Button(main_container, text="◀ BACK TO MAIN MENU", 
                               command=self.reset_to_main_menu,
                               bg='#d32f2f', fg='white', font=self.header_font,
                               padx=20, pady=5, cursor="hand2")
        back_button.pack(pady=(10, 0))
    
    def setup_domain_info_tab(self):
        """Setup domain information tab"""
        # Create scrollable frame
        canvas = tk.Canvas(self.domain_info_frame, bg='#1e1e1e', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.domain_info_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Domain info fields
        self.domain_info_fields = {}
        info_items = [
            "Domain Name", "Status", "Creation Date", "Expiration Date", 
            "Updated Date", "Name Servers", "Domain Age", "Days Until Expiry"
        ]
        
        for i, item in enumerate(info_items):
            frame = tk.Frame(scrollable_frame, bg='#1e1e1e')
            frame.pack(fill=tk.X, pady=5, padx=10)
            
            tk.Label(frame, text=f"{item}:", font=self.header_font, 
                    bg='#1e1e1e', fg='#00ff00', width=20, anchor=tk.W).pack(side=tk.LEFT)
            
            value_label = tk.Label(frame, text="Not checked yet", font=self.text_font,
                                  bg='#1e1e1e', fg='#ffffff', anchor=tk.W)
            value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.domain_info_fields[item] = value_label
    
    def setup_contact_tab(self, parent, contact_type):
        """Setup contact information tab"""
        canvas = tk.Canvas(parent, bg='#1e1e1e', highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        fields = ["Name", "Organization", "Email", "Phone", "Fax", "Address", "City", "State", "Country", "Postal Code"]
        
        contact_fields = {}
        for field in fields:
            frame = tk.Frame(scrollable_frame, bg='#1e1e1e')
            frame.pack(fill=tk.X, pady=5, padx=10)
            
            tk.Label(frame, text=f"{field}:", font=self.header_font,
                    bg='#1e1e1e', fg='#00ff00', width=20, anchor=tk.W).pack(side=tk.LEFT)
            
            value_label = tk.Label(frame, text="Not checked yet", font=self.text_font,
                                  bg='#1e1e1e', fg='#ffffff', anchor=tk.W, wraplength=600,
                                  justify=tk.LEFT)
            value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            contact_fields[field] = value_label
        
        # Store in a dictionary keyed by contact type
        if not hasattr(self, 'contact_fields'):
            self.contact_fields = {}
        self.contact_fields[contact_type] = contact_fields
    
    def setup_registrar_tab(self):
        """Setup registrar information tab"""
        scrollable_frame = self.create_scrollable_frame(self.registrar_frame)
        
        registrar_fields = [
            "Registrar Name", "Registrar IANA ID", "Registrar URL", 
            "WHOIS Server", "Referral URL", "Abuse Contact Email", 
            "Abuse Contact Phone", "Registration System"
        ]
        
        self.registrar_fields = {}
        for field in registrar_fields:
            frame = tk.Frame(scrollable_frame, bg='#1e1e1e')
            frame.pack(fill=tk.X, pady=5, padx=10)
            
            tk.Label(frame, text=f"{field}:", font=self.header_font,
                    bg='#1e1e1e', fg='#00ff00', width=20, anchor=tk.W).pack(side=tk.LEFT)
            
            value_label = tk.Label(frame, text="Not checked yet", font=self.text_font,
                                  bg='#1e1e1e', fg='#ffffff', anchor=tk.W, wraplength=600)
            value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.registrar_fields[field] = value_label
    
    def setup_security_tab(self):
        """Setup DNSSEC and security tab"""
        scrollable_frame = self.create_scrollable_frame(self.security_frame)
        
        security_fields = [
            "DNSSEC Status", "DNSSEC Algorithms", "DS Records", "DNSKEY Records",
            "SSL/TLS Status", "DMARC Record", "SPF Record", "Security Threats"
        ]
        
        self.security_fields = {}
        for field in security_fields:
            frame = tk.Frame(scrollable_frame, bg='#1e1e1e')
            frame.pack(fill=tk.X, pady=5, padx=10)
            
            tk.Label(frame, text=f"{field}:", font=self.header_font,
                    bg='#1e1e1e', fg='#00ff00', width=20, anchor=tk.W).pack(side=tk.LEFT)
            
            value_label = tk.Label(frame, text="Not checked yet", font=self.text_font,
                                  bg='#1e1e1e', fg='#ffffff', anchor=tk.W, wraplength=600)
            value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.security_fields[field] = value_label
    
    def setup_raw_tab(self):
        """Setup raw WHOIS data tab"""
        self.raw_text = scrolledtext.ScrolledText(self.raw_frame, wrap=tk.WORD,
                                                   font=self.text_font, bg='#2d2d2d',
                                                   fg='#00ff00', insertbackground='white')
        self.raw_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_scrollable_frame(self, parent):
        """Create a scrollable frame"""
        canvas = tk.Canvas(parent, bg='#1e1e1e', highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return scrollable_frame
    
    def search_domain(self):
        """Initiate domain search"""
        domain = self.domain_entry.get().strip()
        
        if not domain:
            messagebox.showwarning("Input Error", "Please enter a domain name")
            return
        
        # Validate domain format
        if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', domain):
            messagebox.showwarning("Invalid Domain", "Please enter a valid domain name (e.g., example.com)")
            return
        
        # Get selected provider
        provider_key = self.provider_var.get()
        provider = self.providers[provider_key]
        
        # Start search in separate thread
        self.search_button.config(state=tk.DISABLED, text="🔍 SEARCHING...")
        self.progress.pack(side=tk.LEFT, padx=10)
        self.progress.start(10)
        self.status_bar.config(text=f"Searching for {domain} using {provider['name']}...")
        
        thread = threading.Thread(target=self.perform_lookup, args=(domain, provider))
        thread.daemon = True
        thread.start()
    
    def perform_lookup(self, domain, provider):
        """Perform the actual domain lookup"""
        try:
            result = provider["method"](domain)
            self.current_result = result
            self.root.after(0, self.display_results, result)
        except Exception as e:
            self.root.after(0, self.show_error, str(e))
        finally:
            self.root.after(0, self.search_complete)
    
    def lookup_standard_whois(self, domain: str) -> Dict:
        """Standard WHOIS lookup using python-whois"""
        try:
            w = whois.whois(domain)
            
            # Parse the response
            result = {
                "domain_name": w.domain_name if w.domain_name else "N/A",
                "status": w.status if w.status else "N/A",
                "creation_date": self.format_date(w.creation_date),
                "expiration_date": self.format_date(w.expiration_date),
                "updated_date": self.format_date(w.updated_date),
                "name_servers": w.name_servers if w.name_servers else [],
                "registrar": w.registrar if w.registrar else "N/A",
                "registrar_iana_id": w.registrar_iana_id if hasattr(w, 'registrar_iana_id') else "N/A",
                "registrar_url": w.registrar_url if hasattr(w, 'registrar_url') else "N/A",
                "whois_server": w.whois_server if w.whois_server else "N/A",
                "registrant_name": w.name if w.name else "Redacted/Private",
                "registrant_organization": w.org if w.org else "Redacted/Private",
                "registrant_email": w.emails if w.emails else "Redacted/Private",
                "registrant_phone": w.phone if w.phone else "Redacted/Private",
                "registrant_address": w.address if hasattr(w, 'address') else "N/A",
                "registrant_city": w.city if hasattr(w, 'city') else "N/A",
                "registrant_state": w.state if hasattr(w, 'state') else "N/A",
                "registrant_country": w.country if w.country else "N/A",
                "dnssec": w.dnssec if hasattr(w, 'dnssec') else "unsigned",
                "raw_text": str(w),
                "provider": "Standard WHOIS"
            }
            
            # Add domain age and days until expiry
            result["domain_age"] = self.calculate_age(result["creation_date"])
            result["days_until_expiry"] = self.calculate_days_until_expiry(result["expiration_date"])
            
            # Check DNSSEC
            result["dnssec_status"] = self.check_dnssec(domain)
            
            return result
            
        except Exception as e:
            raise Exception(f"WHOIS lookup failed: {str(e)}")
    
    def lookup_whoisxml(self, domain: str) -> Dict:
        """WHOIS lookup using WhoisXML API (requires API key)"""
        # Note: This requires a free API key from https://whoisxmlapi.com/
        api_key = "YOUR_API_KEY"  # Replace with your actual API key
        
        if api_key == "YOUR_API_KEY":
            # Fallback to standard WHOIS
            return self.lookup_standard_whois(domain)
        
        url = f"https://www.whoisxmlapi.com/whoisserver/WhoisService"
        params = {
            "apiKey": api_key,
            "domainName": domain,
            "outputFormat": "JSON"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            # Parse and format similarly to standard WHOIS
            whois_data = data.get("WhoisRecord", {})
            registrant = whois_data.get("registrant", {})
            administrative = whois_data.get("administrativeContact", {})
            technical = whois_data.get("technicalContact", {})
            
            result = {
                "domain_name": whois_data.get("domainName", "N/A"),
                "status": whois_data.get("status", "N/A"),
                "creation_date": whois_data.get("createdDate", "N/A"),
                "expiration_date": whois_data.get("expiryDate", "N/A"),
                "updated_date": whois_data.get("updatedDate", "N/A"),
                "name_servers": whois_data.get("nameServers", {}).get("hostNames", []),
                "registrar": whois_data.get("registrarName", "N/A"),
                "registrar_iana_id": whois_data.get("registryData", {}).get("ianaId", "N/A"),
                "registrar_url": whois_data.get("registrarWebsite", "N/A"),
                "whois_server": whois_data.get("whoisServer", "N/A"),
                "registrant_name": registrant.get("name", "Redacted"),
                "registrant_organization": registrant.get("organization", "Redacted"),
                "registrant_email": registrant.get("email", "Redacted"),
                "registrant_phone": registrant.get("telephone", "Redacted"),
                "registrant_address": registrant.get("streetAddress1", "N/A"),
                "registrant_city": registrant.get("city", "N/A"),
                "registrant_state": registrant.get("state", "N/A"),
                "registrant_country": registrant.get("country", "N/A"),
                "dnssec": whois_data.get("dnssec", "unsigned"),
                "raw_text": json.dumps(data, indent=2),
                "provider": "WhoisXML API"
            }
            
            result["domain_age"] = self.calculate_age(result["creation_date"])
            result["days_until_expiry"] = self.calculate_days_until_expiry(result["expiration_date"])
            result["dnssec_status"] = self.check_dnssec(domain)
            
            # Add additional contacts
            result["technical_contact"] = technical
            result["administrative_contact"] = administrative
            
            return result
            
        except Exception as e:
            return self.lookup_standard_whois(domain)
    
    def lookup_ipinfo(self, domain: str) -> Dict:
        """WHOIS lookup using IPInfo.io WHOIS API"""
        url = f"https://ipinfo.io/whois/{domain}"
        
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            
            # Parse the response
            result = {
                "domain_name": domain,
                "status": "Not specified",
                "creation_date": data.get("creation_date", "N/A"),
                "expiration_date": data.get("expiration_date", "N/A"),
                "updated_date": data.get("updated_date", "N/A"),
                "name_servers": data.get("nameservers", []),
                "registrar": data.get("registrar", "N/A"),
                "registrar_iana_id": "N/A",
                "registrar_url": data.get("referral_url", "N/A"),
                "whois_server": data.get("whois_server", "N/A"),
                "registrant_name": data.get("registrant", "Redacted"),
                "registrant_organization": data.get("registrant", "Redacted"),
                "registrant_email": data.get("emails", ["Redacted"])[0],
                "registrant_phone": data.get("phone", "Redacted"),
                "registrant_country": data.get("country", "N/A"),
                "dnssec": "Not specified",
                "raw_text": json.dumps(data, indent=2),
                "provider": "IPInfo.io WHOIS"
            }
            
            result["domain_age"] = self.calculate_age(result["creation_date"])
            result["days_until_expiry"] = self.calculate_days_until_expiry(result["expiration_date"])
            result["dnssec_status"] = self.check_dnssec(domain)
            
            return result
            
        except Exception as e:
            return self.lookup_standard_whois(domain)
    
    def lookup_securitytrails(self, domain: str) -> Dict:
        """WHOIS lookup using SecurityTrails API (requires API key)"""
        # Note: Get free API key from https://securitytrails.com/
        api_key = "YOUR_API_KEY"  # Replace with your actual API key
        
        if api_key == "YOUR_API_KEY":
            return self.lookup_standard_whois(domain)
        
        url = f"https://api.securitytrails.com/v1/domain/{domain}/whois"
        headers = {"APIKEY": api_key}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()
            
            result = {
                "domain_name": data.get("domain", "N/A"),
                "status": data.get("status", "N/A"),
                "creation_date": data.get("created_date", "N/A"),
                "expiration_date": data.get("expires_date", "N/A"),
                "updated_date": data.get("updated_date", "N/A"),
                "name_servers": data.get("name_servers", []),
                "registrar": data.get("registrar_name", "N/A"),
                "registrar_iana_id": data.get("registrar_iana_id", "N/A"),
                "registrar_url": "N/A",
                "whois_server": "N/A",
                "registrant_name": data.get("registrant_name", "Redacted"),
                "registrant_organization": data.get("registrant_organization", "Redacted"),
                "registrant_email": data.get("registrant_email", "Redacted"),
                "registrant_phone": data.get("registrant_phone", "Redacted"),
                "registrant_country": data.get("registrant_country", "N/A"),
                "dnssec": data.get("dnssec", "unsigned"),
                "raw_text": json.dumps(data, indent=2),
                "provider": "SecurityTrails"
            }
            
            result["domain_age"] = self.calculate_age(result["creation_date"])
            result["days_until_expiry"] = self.calculate_days_until_expiry(result["expiration_date"])
            result["dnssec_status"] = self.check_dnssec(domain)
            
            return result
            
        except Exception as e:
            return self.lookup_standard_whois(domain)
    
    def check_dnssec(self, domain: str) -> str:
        """Check DNSSEC status for the domain"""
        try:
            # Try to get DNSKEY records
            resolver = dns.resolver.Resolver()
            resolver.timeout = 5
            resolver.lifetime = 5
            
            try:
                answers = resolver.resolve(domain, 'DNSKEY')
                if answers:
                    return "signed (DNSSEC enabled)"
            except:
                pass
            
            # Check for DS records
            try:
                # For .com/.net domains, check parent zone
                resolver.resolve(domain, 'DS')
                return "signed (DS records found)"
            except:
                pass
            
            return "unsigned (DNSSEC not enabled)"
            
        except Exception:
            return "Unable to determine"
    
    def format_date(self, date) -> str:
        """Format date for display"""
        if not date:
            return "N/A"
        
        if isinstance(date, list):
            date = date[0]
        
        if hasattr(date, 'strftime'):
            return date.strftime("%Y-%m-%d %H:%M:%S")
        
        return str(date)
    
    def calculate_age(self, creation_date: str) -> str:
        """Calculate domain age"""
        if not creation_date or creation_date == "N/A":
            return "Unknown"
        
        try:
            if isinstance(creation_date, str):
                # Try to parse various date formats
                for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d-%b-%Y", "%Y-%m-%dT%H:%M:%S"]:
                    try:
                        creation = datetime.strptime(creation_date, fmt)
                        break
                    except:
                        continue
                else:
                    return "Unknown"
            else:
                creation = creation_date
            
            age = datetime.now() - creation
            years = age.days // 365
            months = (age.days % 365) // 30
            days = age.days % 30
            
            return f"{years} years, {months} months, {days} days"
        except:
            return "Unknown"
    
    def calculate_days_until_expiry(self, expiration_date: str) -> str:
        """Calculate days until domain expiration"""
        if not expiration_date or expiration_date == "N/A":
            return "Unknown"
        
        try:
            if isinstance(expiration_date, str):
                for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d-%b-%Y"]:
                    try:
                        expiry = datetime.strptime(expiration_date, fmt)
                        break
                    except:
                        continue
                else:
                    return "Unknown"
            else:
                expiry = expiration_date
            
            days_left = (expiry - datetime.now()).days
            
            if days_left < 0:
                return f"Expired {abs(days_left)} days ago"
            elif days_left == 0:
                return "Expires today"
            else:
                return f"{days_left} days"
        except:
            return "Unknown"
    
    def display_results(self, result: Dict):
        """Display lookup results in the GUI"""
        
        # Update Domain Information tab
        self.update_domain_info(result)
        
        # Update Contact tabs
        self.update_contact_info(result)
        
        # Update Registrar tab
        self.update_registrar_info(result)
        
        # Update Security tab
        self.update_security_info(result)
        
        # Update Raw WHOIS tab
        self.update_raw_whois(result)
        
        # Show success message
        self.status_bar.config(text=f"✓ Successfully retrieved WHOIS data for {result.get('domain_name', 'domain')}")
        
        # Switch to first tab
        self.notebook.select(0)
    
    def update_domain_info(self, result: Dict):
        """Update domain information display"""
        domain_info = {
            "Domain Name": result.get("domain_name", "N/A"),
            "Status": result.get("status", "N/A"),
            "Creation Date": result.get("creation_date", "N/A"),
            "Expiration Date": result.get("expiration_date", "N/A"),
            "Updated Date": result.get("updated_date", "N/A"),
            "Name Servers": "\n".join(result.get("name_servers", [])) if isinstance(result.get("name_servers"), list) else result.get("name_servers", "N/A"),
            "Domain Age": result.get("domain_age", "Unknown"),
            "Days Until Expiry": result.get("days_until_expiry", "Unknown")
        }
        
        for field, value in domain_info.items():
            if field in self.domain_info_fields:
                self.domain_info_fields[field].config(text=str(value), wraplength=600)
    
    def update_contact_info(self, result: Dict):
        """Update contact information display"""
        # Registrant Contact
        registrant_fields = {
            "Name": result.get("registrant_name", "N/A"),
            "Organization": result.get("registrant_organization", "N/A"),
            "Email": result.get("registrant_email", "N/A"),
            "Phone": result.get("registrant_phone", "N/A"),
            "Fax": result.get("registrant_fax", "N/A"),
            "Address": result.get("registrant_address", "N/A"),
            "City": result.get("registrant_city", "N/A"),
            "State": result.get("registrant_state", "N/A"),
            "Country": result.get("registrant_country", "N/A"),
            "Postal Code": result.get("registrant_postal_code", "N/A")
        }
        
        if "Registrant" in self.contact_fields:
            for field, value in registrant_fields.items():
                if field in self.contact_fields["Registrant"]:
                    self.contact_fields["Registrant"][field].config(text=str(value), wraplength=600)
        
        # Technical Contact (if available)
        if "technical_contact" in result:
            tech = result["technical_contact"]
            tech_fields = {
                "Name": tech.get("name", "N/A"),
                "Organization": tech.get("organization", "N/A"),
                "Email": tech.get("email", "N/A"),
                "Phone": tech.get("telephone", "N/A"),
                "Address": tech.get("streetAddress1", "N/A"),
                "City": tech.get("city", "N/A"),
                "Country": tech.get("country", "N/A")
            }
            
            if "Technical" in self.contact_fields:
                for field, value in tech_fields.items():
                    if field in self.contact_fields["Technical"]:
                        self.contact_fields["Technical"][field].config(text=str(value), wraplength=600)
        
        # Administrative Contact (if available)
        if "administrative_contact" in result:
            admin = result["administrative_contact"]
            admin_fields = {
                "Name": admin.get("name", "N/A"),
                "Organization": admin.get("organization", "N/A"),
                "Email": admin.get("email", "N/A"),
                "Phone": admin.get("telephone", "N/A"),
                "Address": admin.get("streetAddress1", "N/A"),
                "City": admin.get("city", "N/A"),
                "Country": admin.get("country", "N/A")
            }
            
            if "Administrative" in self.contact_fields:
                for field, value in admin_fields.items():
                    if field in self.contact_fields["Administrative"]:
                        self.contact_fields["Administrative"][field].config(text=str(value), wraplength=600)
    
    def update_registrar_info(self, result: Dict):
        """Update registrar information display"""
        registrar_fields = {
            "Registrar Name": result.get("registrar", "N/A"),
            "Registrar IANA ID": result.get("registrar_iana_id", "N/A"),
            "Registrar URL": result.get("registrar_url", "N/A"),
            "WHOIS Server": result.get("whois_server", "N/A"),
            "Referral URL": result.get("referral_url", "N/A"),
            "Abuse Contact Email": result.get("abuse_email", "N/A"),
            "Abuse Contact Phone": result.get("abuse_phone", "N/A"),
            "Registration System": result.get("provider", "N/A")
        }
        
        for field, value in registrar_fields.items():
            if field in self.registrar_fields:
                self.registrar_fields[field].config(text=str(value), wraplength=600)
    
    def update_security_info(self, result: Dict):
        """Update security/DNSSEC information display"""
        security_fields = {
            "DNSSEC Status": result.get("dnssec_status", result.get("dnssec", "Unknown")),
            "DNSSEC Algorithms": "Check DNSKEY records",
            "DS Records": "Check parent zone",
            "DNSKEY Records": "Use dig to verify",
            "SSL/TLS Status": "Check certificate",
            "DMARC Record": "Check _dmarc TXT record",
            "SPF Record": "Check TXT record",
            "Security Threats": "No known threats"
        }
        
        for field, value in security_fields.items():
            if field in self.security_fields:
                self.security_fields[field].config(text=str(value), wraplength=600)
    
    def update_raw_whois(self, result: Dict):
        """Update raw WHOIS data display"""
        self.raw_text.delete(1.0, tk.END)
        
        # Format raw data
        raw_data = f"""WHOIS Lookup Results
{'='*60}
Provider: {result.get('provider', 'Unknown')}
Domain: {result.get('domain_name', 'N/A')}
Lookup Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

Raw WHOIS Data:
{'-'*60}
{result.get('raw_text', 'No raw data available')}
"""
        self.raw_text.insert(1.0, raw_data)
    
    def show_error(self, error_msg: str):
        """Show error message"""
        messagebox.showerror("Lookup Error", f"Failed to lookup domain:\n{error_msg}")
        self.status_bar.config(text=f"Error: {error_msg}")
        
        # Clear results
        self.clear_results()
    
    def clear_results(self):
        """Clear all result displays"""
        # Clear domain info
        for field in self.domain_info_fields.values():
            field.config(text="Not checked yet")
        
        # Clear contact info
        for contact_type in self.contact_fields:
            for field in self.contact_fields[contact_type].values():
                field.config(text="Not checked yet")
        
        # Clear registrar info
        for field in self.registrar_fields.values():
            field.config(text="Not checked yet")
        
        # Clear security info
        for field in self.security_fields.values():
            field.config(text="Not checked yet")
        
        # Clear raw data
        self.raw_text.delete(1.0, tk.END)
    
    def search_complete(self):
        """Clean up after search completes"""
        self.progress.stop()
        self.progress.pack_forget()
        self.search_button.config(state=tk.NORMAL, text="🔍 SEARCH DOMAIN")
    
    def reset_to_main_menu(self):
        """Reset to main menu state"""
        self.domain_entry.delete(0, tk.END)
        self.clear_results()
        self.status_bar.config(text="Ready")
        self.notebook.select(0)
        self.domain_entry.focus()

def main():
    """Main entry point"""
    root = tk.Tk()
    app = DomainLookupGUI(root)
    
    # Set window icon (optional - create your own icon)
    # root.iconbitmap('icon.ico')
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{1200}x{800}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()


def run():
    main()